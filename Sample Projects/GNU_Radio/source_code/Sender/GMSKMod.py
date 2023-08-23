#!/usr/bin/env python
#
# GMSK modulation and demodulation.  
#
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

from gnuradio import gr
from gnuradio import modulation_utils
from math import pi
import Numeric
from pprint import pprint
import inspect

# default values (used in __init__ and add_options)
_def_samples_per_symbol = 2
_def_bt = 0.35
_def_verbose = True
_def_log = True

_def_gain_mu = 0.05
_def_mu = 0.5
_def_freq_error = 0.0
_def_omega_relative_limit = 0.005


# /////////////////////////////////////////////////////////////////////////////
#                              GMSK modulator
# /////////////////////////////////////////////////////////////////////////////

class gmsk_mod(gr.hier_block):

    def __init__(self, fg,
                 samples_per_symbol=_def_samples_per_symbol,
                 bt=_def_bt,
                 verbose=_def_verbose,
                 log=_def_log):
        """
	Hierarchical block for Gaussian Minimum Shift Key (GMSK)
	modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

	@param fg: flow graph
	@type fg: flow graph
	@param samples_per_symbol: samples per baud >= 2
	@type samples_per_symbol: integer
	@param bt: Gaussian filter bandwidth * symbol time
	@type bt: float
        @param verbose: Print information about modulator?
        @type verbose: bool
        @param debug: Print modualtion data to files?
        @type debug: bool       
	"""

        self._fg = fg
        self._samples_per_symbol = samples_per_symbol
        self._bt = bt

        if not isinstance(samples_per_symbol, int) or samples_per_symbol < 2:
            raise TypeError, ("samples_per_symbol must be an integer >= 2, is %r" % (samples_per_symbol,))

	ntaps = 4 * samples_per_symbol			# up to 3 bits in filter at once
	sensitivity = (pi / 2) / samples_per_symbol	# phase change per bit = pi / 2

	# Turn it into NRZ data.
	self.nrz = gr.bytes_to_syms()

	# Form Gaussian filter
        # Generate Gaussian response (Needs to be convolved with window below).
	self.gaussian_taps = gr.firdes.gaussian(
		1,		       # gain
		samples_per_symbol,    # symbol_rate
		bt,		       # bandwidth * symbol time
		ntaps	               # number of taps
		)

	self.sqwave = (1,) * samples_per_symbol       # rectangular window
	self.taps = Numeric.convolve(Numeric.array(self.gaussian_taps),Numeric.array(self.sqwave))
	self.gaussian_filter = gr.interp_fir_filter_fff(samples_per_symbol, self.taps)

	# FM modulation
	self.fmmod = gr.frequency_modulator_fc(sensitivity)
		
        if verbose:
            self._print_verbage()
         
        if log:
            self._setup_logging()

	# Connect & Initialize base class
	self._fg.connect(self.nrz, self.gaussian_filter, self.fmmod)
	#self._fg.connect(self.nrz, self.fmmod)
	gr.hier_block.__init__(self, self._fg, self.nrz, self.fmmod)

    def samples_per_symbol(self):
        return self._samples_per_symbol

    def bits_per_symbol(self=None):     # staticmethod that's also callable on an instance
        return 1
    bits_per_symbol = staticmethod(bits_per_symbol)      # make it a static method.


    def _print_verbage(self):
        print "bits per symbol = %d" % self.bits_per_symbol()
        print "Gaussian filter bt = %.2f" % self._bt


    def _setup_logging(self):
        print "Modulation logging turned on."
        #self._fg.connect(self.nrz,
        #                 gr.file_sink(gr.sizeof_float, "nrz.dat"))
        #self._fg.connect(self.gaussian_filter,
        #                 gr.file_sink(gr.sizeof_float, "gaussian_filter.dat"))
        self._fg.connect(self.fmmod,
                         gr.file_sink(gr.sizeof_gr_complex, "Modulated.dat")) #keep the same file name for TCP socket transmission


    def add_options(parser):
        """
        Adds GMSK modulation-specific options to the standard parser
        """
        parser.add_option("", "--bt", type="float", default=_def_bt,
                          help="set bandwidth-time product [default=%default] (GMSK)")
    add_options=staticmethod(add_options)


    def extract_kwargs_from_options(options):
        """
        Given command line options, create dictionary suitable for passing to __init__
        """
        return modulation_utils.extract_kwargs_from_options(gmsk_mod.__init__,
                                                            ('self', 'fg'), options)
    extract_kwargs_from_options=staticmethod(extract_kwargs_from_options)

