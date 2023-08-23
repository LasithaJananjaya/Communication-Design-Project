"""
differential BPSK demodulation.
"""

from gnuradio import gr, gru, modulation_utils
from math import pi, sqrt
from gnuradio.blksimpl import psk
import cmath
import Numeric
from pprint import pprint

# default values (used in __init__ and add_options)
_def_samples_per_symbol = 2
_def_excess_bw = 0.35
_def_gray_code = True
_def_verbose = True
_def_log = True

_def_costas_alpha = 0.05
_def_gain_mu = 0.03
_def_mu = 0.05
_def_omega_relative_limit = 0.005

# /////////////////////////////////////////////////////////////////////////////
#                             DBPSK demodulator
#
#      Differentially coherent detection of differentially encoded BPSK
# /////////////////////////////////////////////////////////////////////////////

class dbpsk_demod(gr.hier_block):

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
	Hierarchical block for RRC-filtered differential BPSK demodulation

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
            raise TypeError, "samples_per_symbol must be >= 2, is %r" % (samples_per_symbol,)

        arity = pow(2,self.bits_per_symbol())

        # Automatic gain control
        scale = (1.0/16384.0)
        self.pre_scaler = gr.multiply_const_cc(scale)   # scale the signal from full-range to +-1
        #self.agc = gr.agc2_cc(0.6e-1, 1e-3, 1, 1, 100)
        self.agc = gr.feedforward_agc_cc(16, 1.0)

        
        # Costas loop (carrier tracking)
        # FIXME: need to decide how to handle this more generally; do we pull it from higher layer?
        costas_order = 2
        beta = .25 * self._costas_alpha * self._costas_alpha
        self.costas_loop = gr.costas_loop_cc(self._costas_alpha, beta, 0.002, -0.002, costas_order)

        # RRC data filter
        ntaps = 11 * self._samples_per_symbol
        self.rrc_taps = gr.firdes.root_raised_cosine(
            1.0,                      # gain 
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

        # find closest constellation point
        rot = 1
	#rot = .707 + .707j
	#print "psk.constellation[arity]=", psk.constellation[arity]	#chen
        rotated_const = map(lambda pt: pt * rot, psk.constellation[arity])
        print "rotated_const =", rotated_const

        self.diffdec = gr.diff_phasor_cc()
        #self.diffdec = gr.diff_decoder_bb(arity)

        self.slicer = gr.constellation_decoder_cb(rotated_const, range(arity))

        if self._gray_code:
            self.symbol_mapper = gr.map_bb(psk.gray_to_binary[arity])
        else:
            self.symbol_mapper = gr.map_bb(psk.ungray_to_binary[arity])
        
        # unpack the k bit vector into a stream of bits
        self.unpack = gr.unpacked_to_packed_bb(self.bits_per_symbol(), gr.GR_MSB_FIRST)

        if verbose:
            self._print_verbage()

        if log:
            self._setup_logging()

        # Connect and Initialize base class
        #self._fg.connect(self.pre_scaler, self.agc, self.costas_loop,
        #                 self.rrc_filter, self.clock_recovery, self.diffdec,
        #                 self.slicer, self.symbol_mapper, self.unpack)
        self._fg.connect(#self.pre_scaler, self.agc, 
			 self.costas_loop,
                         #self.rrc_filter, self.clock_recovery, 
			 self.diffdec,
                         self.slicer, self.symbol_mapper, self.unpack)

        #gr.hier_block.__init__(self, self._fg, self.pre_scaler, self.unpack)	#chen

        gr.hier_block.__init__(self, self._fg, self.costas_loop, self.unpack)

    def samples_per_symbol(self):
        return self._samples_per_symbol

    def bits_per_symbol(self=None):   # staticmethod that's also callable on an instance
        return 1
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
        #self._fg.connect(self.pre_scaler,
        #                 gr.file_sink(gr.sizeof_gr_complex, "prescaler.dat"))
        #self._fg.connect(self.agc,
        #                 gr.file_sink(gr.sizeof_gr_complex, "agc.dat"))
        #self._fg.connect(self.costas_loop,
        #                 gr.file_sink(gr.sizeof_gr_complex, "costas_loop.dat"))
        #self._fg.connect((self.costas_loop,1),
        #                 gr.file_sink(gr.sizeof_gr_complex, "costas_error.dat"))
        #self._fg.connect(self.rrc_filter,
        #                 gr.file_sink(gr.sizeof_gr_complex, "rrc_filter_Rx.dat"))
        #self._fg.connect(self.clock_recovery,
        #                 gr.file_sink(gr.sizeof_gr_complex, "clock_recovery.dat"))
        #self._fg.connect((self.clock_recovery,1),
        #                 gr.file_sink(gr.sizeof_gr_complex, "clock_recovery_error.dat"))
        #self._fg.connect(self.diffdec,
        #                 gr.file_sink(gr.sizeof_gr_complex, "diffdec.dat"))        
        #self._fg.connect(self.slicer,
        #                gr.file_sink(gr.sizeof_char, "slicer.dat"))
        #self._fg.connect(self.symbol_mapper,
        #                 gr.file_sink(gr.sizeof_char, "symbol_mapper.dat"))
        self._fg.connect(self.unpack,
                         gr.file_sink(gr.sizeof_char, "DBPSKDemod.dat"))
        
    def add_options(parser):
        """
        Adds DBPSK demodulation-specific options to the standard parser
        """
        parser.add_option("", "--excess-bw", type="float", default=_def_excess_bw,
                          help="set RRC excess bandwith factor [default=%default] (PSK)")
        parser.add_option("", "--no-gray-code", dest="gray_code",
                          action="store_false", default=_def_gray_code,
                          help="disable gray coding on modulated bits (PSK)")
        parser.add_option("", "--costas-alpha", type="float", default=None,
                          help="set Costas loop alpha value [default=%default] (PSK)")
        parser.add_option("", "--gain-mu", type="float", default=_def_gain_mu,
                          help="set M&M symbol sync loop gain mu value [default=%default] (GMSK/PSK)")
        parser.add_option("", "--mu", type="float", default=_def_mu,
                          help="set M&M symbol sync loop mu value [default=%default] (GMSK/PSK)")
        parser.add_option("", "--omega-relative-limit", type="float", default=_def_omega_relative_limit,
                          help="M&M clock recovery omega relative limit [default=%default] (GMSK/PSK)")
    add_options=staticmethod(add_options)
    
    def extract_kwargs_from_options(options):
        """
        Given command line options, create dictionary suitable for passing to __init__
        """
        return modulation_utils.extract_kwargs_from_options(
                 dbpsk_demod.__init__, ('self', 'fg'), options)
    extract_kwargs_from_options=staticmethod(extract_kwargs_from_options)

#
# Add these to the mod/demod registry
#
#modulation_utils.add_type_1_mod('dbpsk', dbpsk_mod)
#modulation_utils.add_type_1_demod('dbpsk', dbpsk_demod)
