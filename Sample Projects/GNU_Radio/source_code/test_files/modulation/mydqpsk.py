#!/usr/bin/env python
#
# Copyright 2005,2006 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

# See gnuradio-examples/python/gmsk2 for examples

"""
differential QPSK modulation and demodulation.
"""

from gnuradio import gr, gru, modulation_utils
from math import pi, sqrt
import psk
import cmath
import Numeric
from pprint import pprint

# default values (used in __init__ and add_options)
_def_samples_per_symbol = 2
_def_excess_bw = 0.35
_def_gray_code = True
_def_verbose = True
_def_log = True

_def_costas_alpha = 0.10
_def_gain_mu = 0.03
_def_mu = 0.05
_def_omega_relative_limit = 0.005


# /////////////////////////////////////////////////////////////////////////////
#                           DQPSK modulator
# /////////////////////////////////////////////////////////////////////////////

class dqpsk_mod(gr.hier_block):

    def __init__(self, fg,
                 samples_per_symbol=_def_samples_per_symbol,
                 excess_bw=_def_excess_bw,
                 gray_code=_def_gray_code,
                 verbose=_def_verbose,
                 log=_def_log):
        """
	Hierarchical block for RRC-filtered QPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

	@param fg: flow graph
	@type fg: flow graph
	@param samples_per_symbol: samples per symbol >= 2
	@type samples_per_symbol: integer
	@param excess_bw: Root-raised cosine filter excess bandwidth
	@type excess_bw: float
        @param gray_code: Tell modulator to Gray code the bits
        @type gray_code: bool
        @param verbose: Print information about modulator?
        @type verbose: bool
        @param debug: Print modualtion data to files?
        @type debug: bool
	"""

        self._fg = fg
        self._samples_per_symbol = samples_per_symbol
        self._excess_bw = excess_bw
        self._gray_code = gray_code

        if not isinstance(samples_per_symbol, int) or samples_per_symbol < 2:
            raise TypeError, ("sbp must be an integer >= 2, is %d" % samples_per_symbol)

	ntaps = 11 * samples_per_symbol
 
        arity = pow(2,self.bits_per_symbol())

        # turn bytes into k-bit vectors
        self.bytes2chunks = \
          gr.packed_to_unpacked_bb(self.bits_per_symbol(), gr.GR_MSB_FIRST)

        if self._gray_code:
            self.symbol_mapper = gr.map_bb(psk.binary_to_gray[arity])
        else:
            self.symbol_mapper = gr.map_bb(psk.binary_to_ungray[arity])
            
        self.diffenc = gr.diff_encoder_bb(arity)

        rot = .707 + .707j
        rotated_const = map(lambda pt: pt * rot, psk.constellation[arity])
        self.chunks2symbols = gr.chunks_to_symbols_bc(rotated_const)

        # pulse shaping filter
	self.rrc_taps = gr.firdes.root_raised_cosine(
	    self._samples_per_symbol, # gain  (sps since we're interpolating by sps)
            self._samples_per_symbol, # sampling rate
            1.0,		      # symbol rate
            self._excess_bw,          # excess bandwidth (roll-off factor)
            ntaps)

	self.rrc_filter = gr.interp_fir_filter_ccf(self._samples_per_symbol, self.rrc_taps)

        if verbose:
            self._print_verbage()
        
        if log:
            self._setup_logging()
            
	# Connect & Initialize base class
        self._fg.connect(self.bytes2chunks, self.symbol_mapper, self.diffenc,
                         self.chunks2symbols, self.rrc_filter)
	gr.hier_block.__init__(self, self._fg, self.bytes2chunks, self.rrc_filter)

    def samples_per_symbol(self):
        return self._samples_per_symbol

    def bits_per_symbol(self=None):   # staticmethod that's also callable on an instance
        return 2
    bits_per_symbol = staticmethod(bits_per_symbol)      # make it a static method.  RTFM

    def _print_verbage(self):
        print "bits per symbol = %d" % self.bits_per_symbol()
        print "Gray code = %s" % self._gray_code
        print "RRS roll-off factor = %f" % self._excess_bw

    def _setup_logging(self):
        print "Modulation logging turned on."
        self._fg.connect(self.bytes2chunks,
                         gr.file_sink(gr.sizeof_char, "bytes2chunks.dat"))
        self._fg.connect(self.symbol_mapper,
                         gr.file_sink(gr.sizeof_char, "graycoder.dat"))
        self._fg.connect(self.diffenc,
                         gr.file_sink(gr.sizeof_char, "diffenc.dat"))        
        self._fg.connect(self.chunks2symbols,
                         gr.file_sink(gr.sizeof_gr_complex, "chunks2symbols.dat"))
        self._fg.connect(self.rrc_filter,
                         gr.file_sink(gr.sizeof_gr_complex, "rrc_filter.dat"))

    def add_options(parser):
        """
        Adds QPSK modulation-specific options to the standard parser
        """
        parser.add_option("", "--excess-bw", type="float", default=_def_excess_bw,
                          help="set RRC excess bandwith factor [default=%default] (PSK)")
        parser.add_option("", "--no-gray-code", dest="gray_code",
                          action="store_false", default=_def_gray_code,
                          help="disable gray coding on modulated bits (PSK)")
    add_options=staticmethod(add_options)


    def extract_kwargs_from_options(options):
        """
        Given command line options, create dictionary suitable for passing to __init__
        """
        return modulation_utils.extract_kwargs_from_options(dqpsk_mod.__init__,
                                                            ('self', 'fg'), options)
    extract_kwargs_from_options=staticmethod(extract_kwargs_from_options)


# /////////////////////////////////////////////////////////////////////////////
#                           DQPSK demodulator
#
# Differentially coherent detection of differentially encoded qpsk
# /////////////////////////////////////////////////////////////////////////////

class dqpsk_demod(gr.hier_block):

    def __init__(self, fg,
                 samples_per_symbol=_def_samples_per_symbol,
                 excess_bw=_def_excess_bw,
                 costas_alpha=_def_costas_alpha,
                 gain_mu=_def_gain_mu,
                 mu=_def_mu,
                 omega_relative_limit=_def_omega_relative_limit,
                 gray_code=_def_gray_code,
                 verbose=_def_verbose,
                 log=_def_log):
        """
	Hierarchical block for RRC-filtered DQPSK demodulation

	The input is the complex modulated signal at baseband.
	The output is a stream of bits packed 1 bit per byte (LSB)

	@param fg: flow graph
	@type fg: flow graph
	@param samples_per_symbol: samples per symbol >= 2
	@type samples_per_symbol: float
	@param excess_bw: Root-raised cosine filter excess bandwidth
	@type excess_bw: float
        @param costas_alpha: loop filter gain
        @type costas_alphas: float
        @param gain_mu: for M&M block
        @type gain_mu: float
        @param mu: for M&M block
        @type mu: float
        @param omega_relative_limit: for M&M block
        @type omega_relative_limit: float
        @param gray_code: Tell modulator to Gray code the bits
        @type gray_code: bool
        @param verbose: Print information about modulator?
        @type verbose: bool
        @param debug: Print modualtion data to files?
        @type debug: bool
	"""

        self._fg = fg
        self._samples_per_symbol = samples_per_symbol
        self._excess_bw = excess_bw
        self._costas_alpha = costas_alpha
        self._gain_mu = gain_mu
        self._mu = mu
        self._omega_relative_limit = omega_relative_limit
        self._gray_code = gray_code

        if samples_per_symbol < 2:
            raise TypeError, "sbp must be >= 2, is %d" % samples_per_symbol

        arity = pow(2,self.bits_per_symbol())
 
        # Automatic gain control
        scale = (1.0/16384.0)
        self.pre_scaler = gr.multiply_const_cc(scale)   # scale the signal from full-range to +-1
        #self.agc = gr.agc2_cc(0.6e-1, 1e-3, 1, 1, 100)
        self.agc = gr.feedforward_agc_cc(16, 1.0)
       
        # Costas loop (carrier tracking)
        # FIXME: need to decide how to handle this more generally; do we pull it from higher layer?
        costas_order = 4
        beta = .25 * self._costas_alpha * self._costas_alpha
        #self.costas_loop = gr.costas_loop_cc(self._costas_alpha, beta, 0.1, -0.1, costas_order)
        self.costas_loop = gr.costas_loop_cc(self._costas_alpha, beta, 0.002, -0.002, costas_order)

        # RRC data filter
        ntaps = 11 * samples_per_symbol
        self.rrc_taps = gr.firdes.root_raised_cosine(
            self._samples_per_symbol, # gain
            self._samples_per_symbol, # sampling rate
            1.0,                      # symbol rate
            self._excess_bw,          # excess bandwidth (roll-off factor)
            ntaps)

        self.rrc_filter=gr.fir_filter_ccf(1, self.rrc_taps)

        # symbol clock recovery
        omega = self._samples_per_symbol
        gain_omega = .25 * self._gain_mu * self._gain_mu
        self.clock_recovery=gr.clock_recovery_mm_cc(omega, gain_omega,
                                                    self._mu, self._gain_mu,
                                                    self._omega_relative_limit)

        self.diffdec = gr.diff_phasor_cc()
        #self.diffdec = gr.diff_decoder_bb(arity)

        # find closest constellation point
        rot = 1
        #rot = .707 + .707j
        rotated_const = map(lambda pt: pt * rot, psk.constellation[arity])
        #print "rotated_const = %s" % rotated_const

        self.slicer = gr.constellation_decoder_cb(rotated_const, range(arity))

        if self._gray_code:
            self.symbol_mapper = gr.map_bb(psk.gray_to_binary[arity])
        else:
            self.symbol_mapper = gr.map_bb(psk.ungray_to_binary[arity])

        
        # unpack the k bit vector into a stream of bits
        self.unpack = gr.unpack_k_bits_bb(self.bits_per_symbol())

        if verbose:
            self._print_verbage()
        
        if log:
            self._setup_logging()
 
        # Connect & Initialize base class
        self._fg.connect(self.pre_scaler, self.agc, self.costas_loop,
                         self.rrc_filter, self.clock_recovery,
                         self.diffdec, self.slicer, self.symbol_mapper,
                         self.unpack)
        gr.hier_block.__init__(self, self._fg, self.pre_scaler, self.unpack)

    def samples_per_symbol(self):
        return self._samples_per_symbol

    def bits_per_symbol(self=None):   # staticmethod that's also callable on an instance
        return 2
    bits_per_symbol = staticmethod(bits_per_symbol)      # make it a static method.  RTFM

    def _print_verbage(self):
        print "bits per symbol = %d"         % self.bits_per_symbol()
        print "Gray code = %s"               % self._gray_code
        print "RRC roll-off factor = %.2f"   % self._excess_bw
        print "Costas Loop alpha = %.5f"     % self._costas_alpha
        print "M&M symbol sync gain = %.5f"  % self._gain_mu
        print "M&M symbol sync mu = %.5f"    % self._mu
        print "M&M omega relative limit = %.5f" % self._omega_relative_limit
        

    def _setup_logging(self):
        print "Modulation logging turned on."
        self._fg.connect(self.pre_scaler,
                         gr.file_sink(gr.sizeof_gr_complex, "prescaler.dat"))
        self._fg.connect(self.agc,
                         gr.file_sink(gr.sizeof_gr_complex, "agc.dat"))
        self._fg.connect(self.costas_loop,
                         gr.file_sink(gr.sizeof_gr_complex, "costas_loop.dat"))
        self._fg.connect((self.costas_loop,1),
                         gr.file_sink(gr.sizeof_gr_complex, "costas_error.dat"))
        self._fg.connect(self.rrc_filter,
                         gr.file_sink(gr.sizeof_gr_complex, "rrc_filter_Rx.dat"))
        self._fg.connect(self.clock_recovery,
                         gr.file_sink(gr.sizeof_gr_complex, "clock_recovery.dat"))
        self._fg.connect((self.clock_recovery,1),
                        gr.file_sink(gr.sizeof_gr_complex, "clock_recovery_error.dat"))
        self._fg.connect(self.diffdec,
                         gr.file_sink(gr.sizeof_gr_complex, "diffdec.dat"))        
        self._fg.connect(self.slicer,
                         gr.file_sink(gr.sizeof_char, "slicer.dat"))
        self._fg.connect(self.symbol_mapper,
                         gr.file_sink(gr.sizeof_char, "gray_decoder.dat"))
        self._fg.connect(self.unpack,
                         gr.file_sink(gr.sizeof_char, "unpack.dat"))

    def add_options(parser):
        """
        Adds modulation-specific options to the standard parser
        """
        parser.add_option("", "--excess-bw", type="float", default=_def_excess_bw,
                          help="set RRC excess bandwith factor [default=%default] (PSK)")
        parser.add_option("", "--no-gray-code", dest="gray_code",
                          action="store_false", default=_def_gray_code,
                          help="disable gray coding on modulated bits (PSK)")
        parser.add_option("", "--costas-alpha", type="float", default=None,
                          help="set Costas loop alpha value [default=%default] (PSK)")
        parser.add_option("", "--gain-mu", type="float", default=_def_gain_mu,
                          help="set M&M symbol sync loop gain mu value [default=%default] (PSK)")
        parser.add_option("", "--mu", type="float", default=_def_mu,
                          help="set M&M symbol sync loop mu value [default=%default] (PSK)")
    add_options=staticmethod(add_options)

    def extract_kwargs_from_options(options):
        """
        Given command line options, create dictionary suitable for passing to __init__
        """
        return modulation_utils.extract_kwargs_from_options(
            dqpsk_demod.__init__, ('self', 'fg'), options)
    extract_kwargs_from_options=staticmethod(extract_kwargs_from_options)


#
# Add these to the mod/demod registry
#
modulation_utils.add_type_1_mod('dqpsk', dqpsk_mod)
modulation_utils.add_type_1_demod('dqpsk', dqpsk_demod)



import binascii
import random

def main():
	fg = gr.flow_graph()
 
    	random.seed()
	data=[0,1,2,3,4]
    	#data = [random.randint(1,100) for i in range(20000)]
    	data[0] = 0 # you know, for the diff encoding stuff
    	bytes_src = gr.vector_source_b(data,False)

	#fg1 = gr.flow_graph()
    	dd=dqpsk_mod(fg)
	#fg2 = gr.flow_graph()
	ee=dqpsk_demod(fg)
	fg.connect(bytes_src,dd,ee)
	print 'before start'
    	fg.start()
	raw_input('Enter to exit: ')
    	fg.stop()
	print 'after start'

#	raw_input('Enter to operate file: ')
	
#	fp = open('./unpack.dat', 'r')
#	binData = fp.read()
#	fp.close()
#        print binascii.b2a_uu(binData)
	#print binData

if __name__ == "__main__":
    main()
