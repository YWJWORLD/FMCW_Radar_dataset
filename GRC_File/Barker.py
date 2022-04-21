#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Barker
# GNU Radio version: v3.8.5.0-6-g57bd109d

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from Barker_waveform import Barker_waveform  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import numpy as np
from gnuradio import qtgui

class Barker(gr.top_block, Qt.QWidget):

    def __init__(self,i,source_amplitude):
        gr.top_block.__init__(self, "Barker")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Barker")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Barker")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.seed = i
        self.save_path = '/home/wjyun/Radar_generator/Examples/Radar_waveform_generation/Barker/record/record'+str(self.seed)+'.bin'
        
        self.tx_gain = tx_gain = 0
        self.source_amplitude = source_amplitude
        self.signal_freq = signal_freq = 200e3
        self.samp_rate = samp_rate = 2e6
        self.rx_gain = rx_gain = 0
        self.code_len = code_len = 13
        self.center_freq = center_freq = 910e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(('addr=166.104.231.198', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_1.set_gain(rx_gain, 0)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('addr=166.104.231.199', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(3e4))
        self.blocks_head_0_0_0 = blocks.head(gr.sizeof_gr_complex*1, 2048*100)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, self.save_path, False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.Barker_waveform_1 = Barker_waveform(
            code_length=code_len,
            samp_rate=samp_rate,
            source_amplitude=self.source_amplitude,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Barker_waveform_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_head_0_0_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_head_0_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.qtgui_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Barker")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_source_amplitude(self):
        return self.source_amplitude

    def set_source_amplitude(self, source_amplitude):
        self.source_amplitude = source_amplitude

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.Barker_waveform_1.set_samp_rate(self.samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_1.set_gain(self.rx_gain, 0)

    def get_code_len(self):
        return self.code_len

    def set_code_len(self, code_len):
        self.code_len = code_len
        self.Barker_waveform_1.set_code_length(self.code_len)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_sink_x_0_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_1.set_center_freq(self.center_freq, 0)





amplitude_range = np.arange(0.002,0.1,0.0025)

def main(top_block_cls=Barker, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    top_blocks = []
    for idx,amp in enumerate(amplitude_range):
        
        my_tb = top_block_cls(idx,amp)
        top_blocks.append(my_tb)
        top_blocks[idx].start()
        time.sleep(1)
        top_blocks[idx].stop()

if __name__ == '__main__':
    main()
