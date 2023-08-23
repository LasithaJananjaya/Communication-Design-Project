#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: v3.8.2.0-57-gd71cd177

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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.ntaps = ntaps = 11*nfilts*sps
        self.excess_bw = excess_bw = 350e-3
        self.time_off = time_off = 1
        self.taps = taps = 1
        self.samp_rate = samp_rate = 32000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts,nfilts,1.0,excess_bw,ntaps)
        self.qpsk = qpsk = digital.constellation_rect([-0.707-0.707j, -0.707+0.707j, 0.707+0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.noise_volt = noise_volt = 100e-6
        self.loop_bw = loop_bw = 62.8e-3
        self.freq_off = freq_off = 0
        self.delay = delay = 50
        self.costas_bw = costas_bw = 62.8e-3
        self.cma_gain = cma_gain = 10e-3

        ##################################################
        # Blocks
        ##################################################
        self._time_off_range = Range(999e-3, 1.001, 100e-6, 1, 200)
        self._time_off_win = RangeWidget(self._time_off_range, self.set_time_off, 'Channel:Timing Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._time_off_win)
        self.qtgui_tab_widget_1 = Qt.QTabWidget()
        self.qtgui_tab_widget_1_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_0)
        self.qtgui_tab_widget_1_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_0.addLayout(self.qtgui_tab_widget_1_grid_layout_0)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_0, 'channel')
        self.qtgui_tab_widget_1_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_1)
        self.qtgui_tab_widget_1_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_1.addLayout(self.qtgui_tab_widget_1_grid_layout_1)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_1, 'clock')
        self.qtgui_tab_widget_1_widget_2 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_2)
        self.qtgui_tab_widget_1_grid_layout_2 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_2.addLayout(self.qtgui_tab_widget_1_grid_layout_2)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_2, 'equilizer')
        self.qtgui_tab_widget_1_widget_3 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_3)
        self.qtgui_tab_widget_1_grid_layout_3 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_3.addLayout(self.qtgui_tab_widget_1_grid_layout_3)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_3, 'frequency correction')
        self.qtgui_tab_widget_1_widget_4 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_4)
        self.qtgui_tab_widget_1_grid_layout_4 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_4.addLayout(self.qtgui_tab_widget_1_grid_layout_4)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_4, 'difference')
        self.top_grid_layout.addWidget(self.qtgui_tab_widget_1)
        self._noise_volt_range = Range(0, 1, 10e-3, 100e-6, 200)
        self._noise_volt_win = RangeWidget(self._noise_volt_range, self.set_noise_volt, 'channel:Noise Voltage', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_volt_win)
        self._loop_bw_range = Range(0, 200e-3, 10e-3, 62.8e-3, 200)
        self._loop_bw_win = RangeWidget(self._loop_bw_range, self.set_loop_bw, 'Time:BW', "counter_slider", float)
        self.top_grid_layout.addWidget(self._loop_bw_win)
        self._freq_off_range = Range(-100e-3, 100e-3, 1e-3, 0, 200)
        self._freq_off_win = RangeWidget(self._freq_off_range, self.set_freq_off, 'Channel:Frequency offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_off_win)
        self._delay_range = Range(0, 100, 1, 50, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, 'delay', "counter_slider", float)
        self.top_grid_layout.addWidget(self._delay_win)
        self._costas_bw_range = Range(0, 1, 10e-3, 62.8e-3, 200)
        self._costas_bw_win = RangeWidget(self._costas_bw_range, self.set_costas_bw, 'Costas', "counter_slider", float)
        self.top_grid_layout.addWidget(self._costas_bw_win)
        self._cma_gain_range = Range(0, 100e-3, 1e-3, 10e-3, 200)
        self._cma_gain_win = RangeWidget(self._cma_gain_range, self.set_cma_gain, 'CMA', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cma_gain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_2 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_2.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_2.enable_grid(False)
        self.qtgui_freq_sink_x_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_2.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_1.addWidget(self._qtgui_freq_sink_x_2_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.qtgui_tab_widget_1_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_0.addWidget(self._qtgui_freq_sink_x_1_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.qtgui_tab_widget_1_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_3.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.qtgui_tab_widget_1_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_2.addWidget(self._qtgui_freq_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.qtgui_tab_widget_1_grid_layout_2.setColumnStretch(c, 1)
        self.output = qtgui.time_sink_f(
            500, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.output.set_update_time(0.10)
        self.output.set_y_axis(-1, 1)

        self.output.set_y_label('Amplitude', "")

        self.output.enable_tags(True)
        self.output.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.output.enable_autoscale(False)
        self.output.enable_grid(False)
        self.output.enable_axis_labels(True)
        self.output.enable_control_panel(False)
        self.output.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.output.set_line_label(i, "Data {0}".format(i))
            else:
                self.output.set_line_label(i, labels[i])
            self.output.set_line_width(i, widths[i])
            self.output.set_line_color(i, colors[i])
            self.output.set_line_style(i, styles[i])
            self.output.set_line_marker(i, markers[i])
            self.output.set_line_alpha(i, alphas[i])

        self._output_win = sip.wrapinstance(self.output.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_layout_4.addWidget(self._output_win)
        self.equilizer_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.equilizer_0.set_update_time(0.10)
        self.equilizer_0.set_y_axis(-2, 2)
        self.equilizer_0.set_x_axis(-2, 2)
        self.equilizer_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.equilizer_0.enable_autoscale(False)
        self.equilizer_0.enable_grid(False)
        self.equilizer_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.equilizer_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.equilizer_0.set_line_label(i, labels[i])
            self.equilizer_0.set_line_width(i, widths[i])
            self.equilizer_0.set_line_color(i, colors[i])
            self.equilizer_0.set_line_style(i, styles[i])
            self.equilizer_0.set_line_marker(i, markers[i])
            self.equilizer_0.set_line_alpha(i, alphas[i])

        self._equilizer_0_win = sip.wrapinstance(self.equilizer_0.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_3.addWidget(self._equilizer_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_3.setColumnStretch(c, 1)
        self.equilizer = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.equilizer.set_update_time(0.10)
        self.equilizer.set_y_axis(-2, 2)
        self.equilizer.set_x_axis(-2, 2)
        self.equilizer.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.equilizer.enable_autoscale(False)
        self.equilizer.enable_grid(False)
        self.equilizer.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.equilizer.set_line_label(i, "Data {0}".format(i))
            else:
                self.equilizer.set_line_label(i, labels[i])
            self.equilizer.set_line_width(i, widths[i])
            self.equilizer.set_line_color(i, colors[i])
            self.equilizer.set_line_style(i, styles[i])
            self.equilizer.set_line_marker(i, markers[i])
            self.equilizer.set_line_alpha(i, alphas[i])

        self._equilizer_win = sip.wrapinstance(self.equilizer.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_2.addWidget(self._equilizer_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_2.setColumnStretch(c, 1)
        self.digital_psk_demod_0 = digital.psk.psk_demod(
            constellation_points=4,
            differential=True,
            samples_per_symbol=2,
            excess_bw=0.35,
            phase_bw=6.28/100.0,
            timing_bw=6.28/100.0,
            mod_code="gray",
            verbose=False,
            log=False)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(4, loop_bw, rrc_taps, 32, 16, 1.5, 1)
        self.digital_map_bb_0 = digital.map_bb([0,1,3,2])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(costas_bw, 4, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(15, 1, cma_gain, 2)
        self.clock = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.clock.set_update_time(0.10)
        self.clock.set_y_axis(-2, 2)
        self.clock.set_x_axis(-2, 2)
        self.clock.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.clock.enable_autoscale(False)
        self.clock.enable_grid(False)
        self.clock.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.clock.set_line_label(i, "Data {0}".format(i))
            else:
                self.clock.set_line_label(i, labels[i])
            self.clock.set_line_width(i, widths[i])
            self.clock.set_line_color(i, colors[i])
            self.clock.set_line_style(i, styles[i])
            self.clock.set_line_marker(i, markers[i])
            self.clock.set_line_alpha(i, alphas[i])

        self._clock_win = sip.wrapinstance(self.clock.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_1.addWidget(self._clock_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_1.setColumnStretch(c, 1)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_off,
            epsilon=time_off,
            taps=[1.0 ],
            noise_seed=0,
            block_tags=False)
        self.channel = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.channel.set_update_time(0.10)
        self.channel.set_y_axis(-2, 2)
        self.channel.set_x_axis(-2, 2)
        self.channel.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.channel.enable_autoscale(False)
        self.channel.enable_grid(False)
        self.channel.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.channel.set_line_label(i, "Data {0}".format(i))
            else:
                self.channel.set_line_label(i, labels[i])
            self.channel.set_line_width(i, widths[i])
            self.channel.set_line_color(i, colors[i])
            self.channel.set_line_style(i, styles[i])
            self.channel.set_line_marker(i, markers[i])
            self.channel.set_line_alpha(i, alphas[i])

        self._channel_win = sip.wrapinstance(self.channel.pyqwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_grid_layout_0.addWidget(self._channel_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_1_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_unpack_k_bits_bb_1 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(2, 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'D:\\Semester 3\\EN2130 - Communication Design Project\\Project\\Test Flow Diagrams\\Textfile1.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'D:\\Semester 3\\EN2130 - Communication Design Project\\Project\\Test Flow Diagrams\\ReceivedText.txt', True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_unpack_k_bits_bb_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_throttle_0_0_1, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_throttle_0_0_1, 0), (self.output, 0))
        self.connect((self.blocks_throttle_1, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_1, 0), (self.blocks_throttle_0_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.channel, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.equilizer, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_psk_demod_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.equilizer_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.clock, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_freq_sink_x_2, 0))
        self.connect((self.digital_psk_demod_0, 0), (self.digital_map_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ntaps(11*self.nfilts*self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_ntaps(11*self.nfilts*self.sps)
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))

    def get_time_off(self):
        return self.time_off

    def set_time_off(self, time_off):
        self.time_off = time_off
        self.channels_channel_model_0.set_timing_offset(self.time_off)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.output.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_2.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt)

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.loop_bw)

    def get_freq_off(self):
        return self.freq_off

    def set_freq_off(self, freq_off):
        self.freq_off = freq_off
        self.channels_channel_model_0.set_frequency_offset(self.freq_off)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_costas_bw(self):
        return self.costas_bw

    def set_costas_bw(self, costas_bw):
        self.costas_bw = costas_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.costas_bw)

    def get_cma_gain(self):
        return self.cma_gain

    def set_cma_gain(self, cma_gain):
        self.cma_gain = cma_gain
        self.digital_cma_equalizer_cc_0.set_gain(self.cma_gain)





def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
