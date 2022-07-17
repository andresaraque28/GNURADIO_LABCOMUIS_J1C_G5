#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: lab31
# Author: labcom
# GNU Radio version: 3.9.5.0

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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class lab31(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "lab31", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("lab31")
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

        self.settings = Qt.QSettings("GNU Radio", "lab31")

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
        self.samp_rate = samp_rate = 20000
        self.inx = inx = 0

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._inx_options = [0, 1, 2]
        # Create the labels list
        self._inx_labels = ['0', '1', '2']
        # Create the combo box
        self._inx_tool_bar = Qt.QToolBar(self)
        self._inx_tool_bar.addWidget(Qt.QLabel("entrada" + ": "))
        self._inx_combo_box = Qt.QComboBox()
        self._inx_tool_bar.addWidget(self._inx_combo_box)
        for _label in self._inx_labels: self._inx_combo_box.addItem(_label)
        self._inx_callback = lambda i: Qt.QMetaObject.invokeMethod(self._inx_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._inx_options.index(i)))
        self._inx_callback(self.inx)
        self._inx_combo_box.currentIndexChanged.connect(
            lambda i: self.set_inx(self._inx_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._inx_tool_bar)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,inx,0)
        self.blocks_selector_0.set_enabled(True)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_SAW_WAVE, 2200, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 2200, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 1200, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_selector_0, 0), (self.audio_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab31")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)

    def get_inx(self):
        return self.inx

    def set_inx(self, inx):
        self.inx = inx
        self._inx_callback(self.inx)
        self.blocks_selector_0.set_input_index(self.inx)




def main(top_block_cls=lab31, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
