import time,math,sys,signal

from scipy import random
from gnuradio import analog, blocks, gr ,filter
from gnuradio.filter import firdes
# from gnuradio.filter import firdes
import epy_block_costas, epy_block_barker, epy_block_polytime, epy_block_polyphase
import sys
import signal

class transmitter_LFM(gr.hier_block2):
    modname = 'LFM'
    def __init__(self, amp, offset, samp_rate, vco_amplitude=1,limit=10000):
        gr.hier_block2.__init__(
            self, "LFM Waveform Block",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.amp = amp
        self.offset = offset
        self.samp_rate = samp_rate
        self.vco_amplitude = vco_amplitude

        ##################################################
        # Blocks
        ##################################################
        self.hilbert_fc_0 = filter.hilbert_fc(50, firdes.WIN_BLACKMAN_hARRIS, 6.76)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, samp_rate, vco_amplitude)
        self.skip = blocks.skiphead(gr.sizeof_gr_complex,random.randint(1,1000000))
        self.limit = blocks.head(gr.sizeof_gr_complex,limit)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_TRI_WAVE, samp_rate/1.3e3, amp, offset, )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.skip,0), (self.limit, 0),(self,0))
        


class transmitter_barker(gr.hier_block2):
    modname = 'Barker'
    def __init__(self, code_length=13, samp_rate=2e6, source_amplitude=1,limit=10000):
        gr.hier_block2.__init__(
            self, "Barker Waveform Block",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.code_length = code_length
        self.samp_rate = samp_rate
        self.source_amplitude = source_amplitude

        ##################################################
        # Variables
        ##################################################
        self.interp = interp = 10
        self.samp_freq = samp_freq = samp_rate/interp

        ##################################################
        # Blocks
        ##################################################
        self.skip = blocks.skiphead(gr.sizeof_gr_complex,random.randint(1,1000000))
        self.limit = blocks.head(gr.sizeof_gr_complex,limit)
        self.epy_block_barker = epy_block_barker.blk(code_length=code_length)
        self.blocks_vector_source_x_1 = blocks.vector_source_f((0, 0, 0), True, 1, [])
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, int(samp_rate/samp_freq))
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, samp_freq, source_amplitude, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.skip,0), (self.limit,0),(self, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.self.epy_block_barker, 0), (self.blocks_repeat_0_0, 0))

class transmitter_costas(gr.hier_block2):
    modname = 'Costas'
    def __init__(self, prime_number=11, primitive_root=2, samp_rate=0, seq_len=1024, source_amplitude=1,limit=10000):
        gr.hier_block2.__init__(
            self, "Costas Waveform Blocks",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.prime_number = prime_number
        self.primitive_root = primitive_root
        self.samp_rate = samp_rate
        self.seq_len = seq_len
        self.source_amplitude = source_amplitude

        ##################################################
        # Variables
        ##################################################
        self.multi_const = multi_const = prime_number-1

        ##################################################
        # Blocks
        ##################################################
        self.skip = blocks.skiphead(gr.sizeof_gr_complex,random.randint(1,1000000))
        self.limit = blocks.head(gr.sizeof_gr_complex,limit)
        self.epy_block_costas = epy_block_costas.blk(primitive_root=primitive_root, prime_number=prime_number)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, samp_rate, source_amplitude)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(seq_len / (prime_number-1)))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0),(self.skip,0), (self.limit,0), (self, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_vco_f_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.epy_block_costas, 0), (self.blocks_repeat_0, 0))

class transmitter_polyphase(gr.hier_block2):
    def __init__(self, code_length=16, kind_of_signal='Frank', samp_freq=2e6/4, samp_rate=2e6, source_amplitude=1,limit=10000):
        gr.hier_block2.__init__(
            self, "Polyphase Waveform Block",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.code_length = code_length
        self.kind_of_signal = kind_of_signal
        self.samp_freq = samp_freq
        self.samp_rate = samp_rate
        self.source_amplitude = source_amplitude

        ##################################################
        # Blocks
        ##################################################
        self.skip = blocks.skiphead(gr.sizeof_gr_complex,random.randint(1,1000000))
        self.limit = blocks.head(gr.sizeof_gr_complex,limit)
        self.epy_block_polyphase = epy_block_polyphase.blk(code_length=code_length, kind_of_signal=kind_of_signal)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, int(samp_rate/samp_freq))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(samp_rate/samp_freq))
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, samp_freq, source_amplitude, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, samp_freq, source_amplitude, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0),(self.skip,0), (self.limit,0), (self, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.epy_block_polyphase, 0), (self.blocks_repeat_0, 0))
        self.connect((self.epy_block_polyphase, 1), (self.blocks_repeat_0_0, 0))

class transmitter_frank(transmitter_polyphase):
    modname = 'Frank'
    def __init__(self, code_length,limit=10000, kind_of_signal=modname,samp_freq=2e6/4,  samp_rate=2e6,  source_amplitude=1):
        super().__init__(code_length, kind_of_signal, samp_freq, samp_rate, source_amplitude,limit)

class transmitter_P1(transmitter_polyphase):
    modname = 'P1'
    def __init__(self, code_length=16,limit=10000, kind_of_signal=modname, samp_freq=2e6/4, samp_rate=2e6, source_amplitude=1):
        super().__init__(code_length, kind_of_signal, samp_freq, samp_rate, source_amplitude,limit)

class transmitter_P2(transmitter_polyphase):
    modname = 'P2'
    def __init__(self, code_length=16,limit=10000, kind_of_signal=modname, samp_freq=2e6/4, samp_rate=2e6, source_amplitude=1):
        super().__init__(code_length, kind_of_signal, samp_freq, samp_rate, source_amplitude,limit)

class transmitter_P3(transmitter_polyphase):
    modname = 'P3'
    def __init__(self, code_length=16,limit=10000, kind_of_signal=modname, samp_freq=2e6/4, samp_rate=2e6, source_amplitude=1):
        super().__init__(code_length, kind_of_signal, samp_freq, samp_rate, source_amplitude,limit)

class transmitter_P4(transmitter_polyphase):
    modname = 'P4'
    def __init__(self, code_length=16,limit=10000, kind_of_signal=modname, samp_freq=2e6/4, samp_rate=2e6, source_amplitude=1):
        super().__init__(code_length, kind_of_signal, samp_freq, samp_rate, source_amplitude,limit)


class transmitter_polytime(gr.hier_block2):
    def __init__(self, Kind_of_signal='T1', center_freq=910e6, delta_f=2000, interp=2e6/500e3, phase_state=2, samp_rate=2e6, segment=4, signal_freq=2e6/4, source_amplitude=1,limit=10000):
        gr.hier_block2.__init__(
            self, "Polytime waveform Block",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.Kind_of_signal = Kind_of_signal
        self.center_freq = center_freq
        self.delta_f = delta_f
        self.interp = interp
        self.phase_state = phase_state
        self.samp_rate = samp_rate
        self.segment = segment
        self.signal_freq = signal_freq
        self.source_amplitude = source_amplitude

        ##################################################
        # Blocks
        ##################################################
        self.skip = blocks.skiphead(gr.sizeof_gr_complex,random.randint(1,1000000))
        self.limit = blocks.head(gr.sizeof_gr_complex,limit)
        self.epy_block_polytime = epy_block_polytime.blk(kind_of_signal=Kind_of_signal, number_of_segment=segment, phase_state=phase_state, delta_f=delta_f, t_seg=0.004, t_interval=0.0001)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, int(interp))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(interp))
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, signal_freq, source_amplitude, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, signal_freq, source_amplitude, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        
        self.connect((self.blocks_float_to_complex_0, 0),(self.skip,0), (self.limit,0),(self, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.epy_block_polytime, 1), (self.blocks_repeat_0, 0))
        self.connect((self.epy_block_polytime, 0), (self.blocks_repeat_0_0, 0))

class transmitter_T1(transmitter_polytime):
    modname = 'T1'
    def __init__(self, Kind_of_signal=modname,limit=10000, center_freq=910e6, delta_f=2000, interp=2e6/500e3, phase_state=2, samp_rate=2e6, segment=4, signal_freq=2e6/4, source_amplitude=1):
        super().__init__(Kind_of_signal, center_freq, delta_f,interp,phase_state, samp_rate,segment, signal_freq, source_amplitude,limit)

class transmitter_T2(transmitter_polytime):
    modname = 'T2'
    def __init__(self, Kind_of_signal=modname,limit=10000, center_freq=910e6, delta_f=2000, interp=2e6/500e3, phase_state=2, samp_rate=2e6, segment=4, signal_freq=2e6/4, source_amplitude=1):
        super().__init__(Kind_of_signal, center_freq, delta_f,interp,phase_state, samp_rate,segment, signal_freq, source_amplitude,limit)

class transmitter_T3(transmitter_polytime):
    modname = 'T3'
    def __init__(self, Kind_of_signal=modname,limit=10000, center_freq=910e6, delta_f=2000, interp=2e6/500e3, phase_state=2, samp_rate=2e6, segment=4, signal_freq=2e6/4, source_amplitude=1):
        super().__init__(Kind_of_signal, center_freq, delta_f,interp,phase_state, samp_rate,segment, signal_freq, source_amplitude,limit)

class transmitter_T4(transmitter_polytime):
    modname = 'T4'
    def __init__(self, Kind_of_signal=modname,limit=10000, center_freq=910e6, delta_f=2000, interp=2e6/500e3, phase_state=2, samp_rate=2e6, segment=4, signal_freq=2e6/4, source_amplitude=1):
        super().__init__(Kind_of_signal, center_freq, delta_f,interp,phase_state, samp_rate,segment, signal_freq, source_amplitude,limit)
    

transmitters = {
    "FMCW_Polyphase":[transmitter_frank,transmitter_P1,transmitter_P2,transmitter_P3,transmitter_P4],
    "FMCW_LFM":[transmitter_LFM],
    "FMCW_Polytime":[transmitter_T1,transmitter_T2,transmitter_T3,transmitter_T4],
    "FMCW_Costas":[transmitter_costas],
    "FMCW_Barker":[transmitter_barker],
    
    
}