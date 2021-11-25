#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: ASK receiver of Keeloq remotes
# Author: Jiri Pittner, OZ9AEC
# Description: ASK receiver of Keeloq at 433.9MHz, based on OZ9AEC's AM receiver
# Generated: Sat Feb 16 21:40:38 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class rx433(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="ASK receiver of Keeloq remotes ")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.width = width = 30000
        self.samp_rate = samp_rate = 64e6/128
        self.offset_fine = offset_fine = 0
        self.offset_coarse = offset_coarse = 0
        self.freq = freq = 318e6
        self.center = center = 0
        self.trans = trans = 1200
        self.rx_freq = rx_freq = freq+(offset_coarse+offset_fine)
        self.rf_gain = rf_gain = 1
        self.low = low = center-width/2
        self.high = high = center+width/2
        self.filter_taps = filter_taps = firdes.low_pass(1, samp_rate, 25000, 2000, firdes.WIN_HAMMING, 6.76)
        self.agc_decay = agc_decay = 10e-6
        self.af_gain = af_gain = 0.9
        self.LO = LO = 0

        ##################################################
        # Blocks
        ##################################################
        _trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._trans_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	label='Trans',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._trans_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	minimum=100,
        	maximum=2000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_trans_sizer, 10, 0, 1, 2)
        self._rx_freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.rx_freq,
        	callback=self.set_rx_freq,
        	label='Receive',
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._rx_freq_static_text, 5, 3, 1, 1)
        _offset_fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_fine_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	label='Offset (fine)',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_fine_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	minimum=-1000,
        	maximum=1000,
        	num_steps=400,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_fine_sizer, 7, 0, 1, 5)
        _offset_coarse_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_coarse_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	label='Offset (coarse)',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_coarse_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	minimum=-100000,
        	maximum=100000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_coarse_sizer, 6, 0, 1, 5)
        self.nbook = self.nbook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "RF Spectrum")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "IF Spectrum")
        self.GridAdd(self.nbook, 0, 0, 5, 5)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label='USRP',
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._freq_text_box, 5, 0, 1, 1)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate/5,
        	v_scale=20,
        	v_offset=0,
        	t_scale=2e-3,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.nbook.GetPage(0).GetWin(),
        	baseband_freq=LO+freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=768,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='RF Spectrum',
        	peak_hold=False,
        	size=(900,300),
        )
        self.nbook.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        _width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._width_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	label='Width',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._width_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	minimum=1000,
        	maximum=100000,
        	num_steps=190,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_width_sizer, 8, 0, 1, 2)
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label='RF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_rf_gain_sizer, 9, 2, 1, 1)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(rx_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(5, (filter_taps), -(offset_coarse+offset_fine), samp_rate)
        _center_sizer = wx.BoxSizer(wx.VERTICAL)
        self._center_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	label='Center',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._center_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	minimum=-5000,
        	maximum=5000,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_center_sizer, 9, 0, 1, 2)
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate/5, low, high, trans, firdes.WIN_HAMMING, 6.76))
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate/5,
        	audio_decim=1,
        	audio_pass=4000,
        	audio_stop=6000,
        )
        self._agc_decay_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.agc_decay,
        	callback=self.set_agc_decay,
        	label='AGC',
        	choices=[100e-6, 50e-6, 10e-6],
        	labels=['Fast', 'Medium', 'Slow'],
        )
        self.GridAdd(self._agc_decay_chooser, 8, 2, 1, 1)
        _af_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._af_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	label='AF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._af_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	minimum=0,
        	maximum=2,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_af_gain_sizer, 10, 2, 1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._width_slider.set_value(self.width)
        self._width_text_box.set_value(self.width)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filter_taps(firdes.low_pass(1, self.samp_rate, 25000, 2000, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/5)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/5, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_offset_fine(self):
        return self.offset_fine

    def set_offset_fine(self, offset_fine):
        self.offset_fine = offset_fine
        self.set_rx_freq(self.freq+(self.offset_coarse+self.offset_fine))
        self._offset_fine_slider.set_value(self.offset_fine)
        self._offset_fine_text_box.set_value(self.offset_fine)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_offset_coarse(self):
        return self.offset_coarse

    def set_offset_coarse(self, offset_coarse):
        self.offset_coarse = offset_coarse
        self.set_rx_freq(self.freq+(self.offset_coarse+self.offset_fine))
        self._offset_coarse_slider.set_value(self.offset_coarse)
        self._offset_coarse_text_box.set_value(self.offset_coarse)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_rx_freq(self.freq+(self.offset_coarse+self.offset_fine))
        self._freq_text_box.set_value(self.freq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.LO+self.freq)

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._center_slider.set_value(self.center)
        self._center_text_box.set_value(self.center)

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self._trans_slider.set_value(self.trans)
        self._trans_text_box.set_value(self.trans)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/5, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self._rx_freq_static_text.set_value(self.rx_freq)
        self.osmosdr_source_0.set_center_freq(self.rx_freq, 0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/5, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_high(self):
        return self.high

    def set_high(self, high):
        self.high = high
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/5, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.filter_taps))

    def get_agc_decay(self):
        return self.agc_decay

    def set_agc_decay(self, agc_decay):
        self.agc_decay = agc_decay
        self._agc_decay_chooser.set_value(self.agc_decay)

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self._af_gain_slider.set_value(self.af_gain)
        self._af_gain_text_box.set_value(self.af_gain)

    def get_LO(self):
        return self.LO

    def set_LO(self, LO):
        self.LO = LO
        self.wxgui_fftsink2_0.set_baseband_freq(self.LO+self.freq)


def main(top_block_cls=rx433, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
