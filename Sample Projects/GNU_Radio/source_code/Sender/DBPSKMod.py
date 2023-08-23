"""
differential BPSK modulation
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
#                             DBPSK modulator
# /////////////////////////////////////////////////////////////////////////////

class dbpsk_mod(gr.hier_block):

    def __init__(self, fg,
		 #arrChenData,
                 samples_per_symbol=_def_samples_per_symbol,
                 excess_bw=_def_excess_bw,
                 gray_code=_def_gray_code,
                 verbose=_def_verbose,
                 log=_def_log):
        """
	Hierarchical block for RRC-filtered differential BPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.
        
	@param fg: flow graph
	@type fg: flow graph
	@param samples_per_symbol: samples per baud >= 2
	@type samples_per_symbol: integer
	@param excess_bw: Root-raised cosine filter excess bandwidth
	@type excess_bw: float
        @param gray_code: Tell modulator to Gray code the bits
        @type gray_code: bool
        @param verbose: Print information about modulator?
        @type verbose: bool
        @param log: Log modulation data to files?
        @type log: bool
	"""

        self._fg = fg
        self._samples_per_symbol = samples_per_symbol
        self._excess_bw = excess_bw
        self._gray_code = gray_code
	#self._arrChenData = arrChenData

        if not isinstance(self._samples_per_symbol, int) or self._samples_per_symbol < 2:
            raise TypeError, ("sbp must be an integer >= 2, is %d" % self._samples_per_symbol)
        
	ntaps = 11 * self._samples_per_symbol

        arity = pow(2,self.bits_per_symbol())
       
        # turn bytes into k-bit vectors
        self.bytes2chunks = \
          gr.packed_to_unpacked_bb(self.bits_per_symbol(), gr.GR_MSB_FIRST)

        if self._gray_code:
            self.symbol_mapper = gr.map_bb(psk.binary_to_gray[arity])
        else:
            self.symbol_mapper = gr.map_bb(psk.binary_to_ungray[arity])

        self.diffenc = gr.diff_encoder_bb(arity)
        
        self.chunks2symbols = gr.chunks_to_symbols_bc(psk.constellation[arity])

        # pulse shaping filter
	self.rrc_taps = gr.firdes.root_raised_cosine(
	    self._samples_per_symbol, # gain  (samples_per_symbol since we're
                                      # interpolating by samples_per_symbol)
	    self._samples_per_symbol, # sampling rate
	    1.0,		      # symbol rate
	    self._excess_bw,          # excess bandwidth (roll-off factor)
            ntaps)

	self.rrc_filter = gr.interp_fir_filter_ccf(self._samples_per_symbol,
                                                   self.rrc_taps)

	# Connect
        #fg.connect(self.bytes2chunks, self.symbol_mapper, self.diffenc,	#chen
        #           self.chunks2symbols, self.rrc_filter)

        fg.connect(self.bytes2chunks, self.symbol_mapper, self.diffenc,
                   self.chunks2symbols)

        if verbose:
            self._print_verbage()
            
        if log:
            self._setup_logging()
            
	# Initialize base class
	#gr.hier_block.__init__(self, self._fg, self.bytes2chunks, self.rrc_filter)	#chen

	gr.hier_block.__init__(self, self._fg, self.bytes2chunks, self.chunks2symbols)

    def samples_per_symbol(self):
        return self._samples_per_symbol

    def bits_per_symbol(self=None):   # static method that's also callable on an instance
        return 1
    bits_per_symbol = staticmethod(bits_per_symbol)      # make it a static method.  RTFM

    def add_options(parser):
        """
        Adds DBPSK modulation-specific options to the standard parser
        """
        parser.add_option("", "--excess-bw", type="float", default=_def_excess_bw,
                          help="set RRC excess bandwith factor [default=%default]")
        parser.add_option("", "--no-gray-code", dest="gray_code",
                          action="store_false", default=True,
                          help="disable gray coding on modulated bits (PSK)")
    add_options=staticmethod(add_options)

    def extract_kwargs_from_options(options):
        """
        Given command line options, create dictionary suitable for passing to __init__
        """
        return modulation_utils.extract_kwargs_from_options(dbpsk_mod.__init__,
                                                            ('self', 'fg'), options)
    extract_kwargs_from_options=staticmethod(extract_kwargs_from_options)


    def _print_verbage(self):
        print "bits per symbol = %d" % self.bits_per_symbol()
        print "Gray code = %s" % self._gray_code
        print "RRC roll-off factor = %.2f" % self._excess_bw

    def _setup_logging(self):
        print "Modulation logging turned on."
        #self._fg.connect(self.bytes2chunks,
        #                 gr.file_sink(gr.sizeof_char, "bytes2chunks.dat"))
        #self._fg.connect(self.symbol_mapper,
        #                 gr.file_sink(gr.sizeof_char, "graycoder.dat"))
        #self._fg.connect(self.diffenc,
        #                 gr.file_sink(gr.sizeof_char, "diffenc.dat"))
        self._fg.connect(self.chunks2symbols,
                         gr.file_sink(gr.sizeof_gr_complex, "Modulated.dat"))
        #self._fg.connect(self.rrc_filter,	#chen
        #                 gr.file_sink(gr.sizeof_gr_complex, "rrc_filter.dat"))
