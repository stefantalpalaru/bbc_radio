#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QPushButton, QMessageBox
#from pprint import pprint
import subprocess
import argparse

# URL list taken from:
# https://garfnet.org.uk/cms/2023/10/29/latest-bbc-hls-radio-streams/

# Parsing command:
# gawk 'BEGIN {FS=","; ORS=""} /EXTINF/ {print "[\""$2"\", "} /^http/ {print "\""$0"\"],\n"}' 20231029-bbc-radio-norewind.m3u.txt
BBC_STATIONS = [
    ["BBC - BBC World Service", "http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/sbr_low/ak/bbc_world_service.m3u8"],
    ["BBC - Radio 1", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_one/bbc_radio_one.isml/bbc_radio_one-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 1Xtra", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_1xtra/bbc_1xtra.isml/bbc_1xtra-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 1Dance", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_one_dance/bbc_radio_one_dance.isml/bbc_radio_one_dance-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 1Relax", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_one_relax/bbc_radio_one_relax.isml/bbc_radio_one_relax-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 2", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_two/bbc_radio_two.isml/bbc_radio_two-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 3", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_three/bbc_radio_three.isml/bbc_radio_three-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 4", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_fourfm/bbc_radio_fourfm.isml/bbc_radio_fourfm-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 4 LW", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_fourlw/bbc_radio_fourlw.isml/bbc_radio_fourlw-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 4 Extra", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_four_extra/bbc_radio_four_extra.isml/bbc_radio_four_extra-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 5 live", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_five_live/bbc_radio_five_live.isml/bbc_radio_five_live-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 6 Music", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_6music/bbc_6music.isml/bbc_6music-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio 5 Live sports extra (UK Only)", "http://as-hls-uk-live.akamaized.net/pool_904/live/uk/bbc_radio_five_live_sports_extra/bbc_radio_five_live_sports_extra.isml/bbc_radio_five_live_sports_extra-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Asian Network", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_asian_network/bbc_asian_network.isml/bbc_asian_network-audio%3d96000.norewind.m3u8"],
    ["BBC - BBC CWR", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_coventry_warwickshire/bbc_radio_coventry_warwickshire.isml/bbc_radio_coventry_warwickshire-audio%3d96000.norewind.m3u8"],
    ["BBC - BBC Essex", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_essex/bbc_radio_essex.isml/bbc_radio_essex-audio%3d96000.norewind.m3u8"],
    ["BBC - BBC Hereford Worcester", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_hereford_worcester/bbc_radio_hereford_worcester.isml/bbc_radio_hereford_worcester-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Berkshire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_berkshire/bbc_radio_berkshire.isml/bbc_radio_berkshire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Bristol", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_bristol/bbc_radio_bristol.isml/bbc_radio_bristol-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Cambridge", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_cambridge/bbc_radio_cambridge.isml/bbc_radio_cambridge-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Cornwall", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_cornwall/bbc_radio_cornwall.isml/bbc_radio_cornwall-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Cumbria", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_cumbria/bbc_radio_cumbria.isml/bbc_radio_cumbria-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Cymru", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_cymru/bbc_radio_cymru.isml/bbc_radio_cymru-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Cymru 2", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_cymru_2/bbc_radio_cymru_2.isml/bbc_radio_cymru_2-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Derby", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_derby/bbc_radio_derby.isml/bbc_radio_derby-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Devon", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_devon/bbc_radio_devon.isml/bbc_radio_devon-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Foyle", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_foyle/bbc_radio_foyle.isml/bbc_radio_foyle-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Gloucestershire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_gloucestershire/bbc_radio_gloucestershire.isml/bbc_radio_gloucestershire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Guernsey", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_guernsey/bbc_radio_guernsey.isml/bbc_radio_guernsey-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Humberside", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_humberside/bbc_radio_humberside.isml/bbc_radio_humberside-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Jersey", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_jersey/bbc_radio_jersey.isml/bbc_radio_jersey-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Kent", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_kent/bbc_radio_kent.isml/bbc_radio_kent-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Lancashire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_lancashire/bbc_radio_lancashire.isml/bbc_radio_lancashire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Leeds", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_leeds/bbc_radio_leeds.isml/bbc_radio_leeds-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Leicester", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_leicester/bbc_radio_leicester.isml/bbc_radio_leicester-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Lincolnshire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_lincolnshire/bbc_radio_lincolnshire.isml/bbc_radio_lincolnshire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio London", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_london/bbc_london.isml/bbc_london-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Manchester", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_manchester/bbc_radio_manchester.isml/bbc_radio_manchester-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Merseyside", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_merseyside/bbc_radio_merseyside.isml/bbc_radio_merseyside-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio nan Gaidheal", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_nan_gaidheal/bbc_radio_nan_gaidheal.isml/bbc_radio_nan_gaidheal-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Newcastle", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_newcastle/bbc_radio_newcastle.isml/bbc_radio_newcastle-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Norfolk", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_norfolk/bbc_radio_norfolk.isml/bbc_radio_norfolk-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Northampton", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_northampton/bbc_radio_northampton.isml/bbc_radio_northampton-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Nottingham", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_nottingham/bbc_radio_nottingham.isml/bbc_radio_nottingham-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Orkney", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_orkney/bbc_radio_orkney.isml/bbc_radio_orkney-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Oxford", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_oxford/bbc_radio_oxford.isml/bbc_radio_oxford-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Scotland FM", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_scotland_fm/bbc_radio_scotland_fm.isml/bbc_radio_scotland_fm-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Scotland MW", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_scotland_mw/bbc_radio_scotland_mw.isml/bbc_radio_scotland_mw-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Sheffield", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_sheffield/bbc_radio_sheffield.isml/bbc_radio_sheffield-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Shropshire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_shropshire/bbc_radio_shropshire.isml/bbc_radio_shropshire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Solent", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_solent/bbc_radio_solent.isml/bbc_radio_solent-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Solent West Dorset", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_solent_west_dorset/bbc_radio_solent_west_dorset.isml/bbc_radio_solent_west_dorset-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Somerset Sound", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_somerset_sound/bbc_radio_somerset_sound.isml/bbc_radio_somerset_sound-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Stoke", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_stoke/bbc_radio_stoke.isml/bbc_radio_stoke-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Suffolk", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_suffolk/bbc_radio_suffolk.isml/bbc_radio_suffolk-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Surrey", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_surrey/bbc_radio_surrey.isml/bbc_radio_surrey-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Sussex", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_sussex/bbc_radio_sussex.isml/bbc_radio_sussex-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Tees", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_tees/bbc_tees.isml/bbc_tees-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Ulster", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_ulster/bbc_radio_ulster.isml/bbc_radio_ulster-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Wales", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_wales_fm/bbc_radio_wales_fm.isml/bbc_radio_wales_fm-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio Wiltshire", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_wiltshire/bbc_radio_wiltshire.isml/bbc_radio_wiltshire-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio WM", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_wm/bbc_wm.isml/bbc_wm-audio%3d96000.norewind.m3u8"],
    ["BBC - Radio York", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_york/bbc_radio_york.isml/bbc_radio_york-audio%3d96000.norewind.m3u8"],
    ["BBC - Three Counties Radio", "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_three_counties_radio/bbc_three_counties_radio.isml/bbc_three_counties_radio-audio%3d96000.norewind.m3u8"],
]

# URL list taken from http://icestreaming.rai.it/status.xsl. Renamed following https://www.raiplayradio.it/
RAI_STATIONS = [
    ['RAI Radio 1', 'http://icestreaming.rai.it/1.mp3'],
    ['RAI Radio 1 Sport', 'http://icestreaming.rai.it/13.mp3'],
    ['RAI Radio 2', 'http://icestreaming.rai.it/2.mp3'],
    ['RAI Radio 2 Indie', 'http://icestreaming.rai.it/15.mp3'],
    ['RAI Radio 3', 'http://icestreaming.rai.it/3.mp3'],
    ['RAI Radio 3 Classica', 'http://icestreaming.rai.it/5.mp3'],
    ['RAI IsoRadio', 'http://icestreaming.rai.it/6.mp3'],
    ['RAI GrParlamento', 'http://icestreaming.rai.it/7.mp3'],
    ['RAI Radio Kids', 'http://icestreaming.rai.it/11.mp3'],
    ['RAI Radio Live', 'http://icestreaming.rai.it/10.mp3'],
    ['RAI Radio Techetè', 'http://icestreaming.rai.it/9.mp3'],
    ['RAI Radio Tutta Italia', 'http://icestreaming.rai.it/11.mp3'],
]

# URL list taken from https://github.com/LaQuay/TDTChannels/blob/master/RADIO.md
SPANISH_STATIONS = [
    ['Radio Nacional RNE', 'https://rtvelivestream.akamaized.net/rtvesec/rne/rne_r1_main.m3u8'],
    ['Radio 3 RNE', 'https://rtvelivestream.akamaized.net/rtvesec/rne/rne_r3_main.m3u8'],
    ['Radio 4 RNE', 'https://rtvelivestream.akamaized.net/rtvesec/rne/rne_r4_main.m3u8'],  
    ['Radio 5 RNE', 'https://rtvelivestream.akamaized.net/rtvesec/rne/rne_r5_madrid_main.m3u8'],    
    ['Cadena SER', 'https://playerservices.streamtheworld.com/api/livestream-redirect/CADENASER.mp3'],
    ['Cadena COPE', 'https://playerservices.streamtheworld.com/api/livestream-redirect/CADENASER.mp3'],
    ['Onda Cero', 'https://atres-live.ondacero.es/live/ondacero/master.m3u8'],
    ['esRadio', 'https://libertaddigital-libremercado-live.flumotion.com/libertaddigital/libremercado-high.mp3'],
    ['Catalunya Radio', 'https://directes-radio-int.ccma.cat/live-content/catalunya-radio-hls/master.m3u8'],
    ['Canal Sur Radio', 'https://cdnlive.codev8.net/rtvalive/smil:channel4.smil/playlist.m3u8'],
    ['Euskadi Irratia', 'https://multimedia.eitb.eus/live-content/euskadirratia-hls/master.m3u8'],
    ['Radio Galega', 'https://crtvg-radiogalega-hls.flumotion.cloud/playlist.m3u8'],
    ['Radiolé', 'https://playerservices.streamtheworld.com/api/livestream-redirect/RADIOLE.mp3'],
    ['Canal Fiesta Radio', 'https://cdnlive.codev8.net/rtvalive/smil:channel5.smil/playlist.m3u8'],
    ['RAC1', 'https://playerservices.streamtheworld.com/api/livestream-redirect/RAC_1.mp3'],
]


WIN_TITLE = "BBC & RAI Radio"

class Win(QMainWindow):
    def __init__(self, parent=None):
        super(Win, self).__init__(parent)
        self.player = None
        # args
        parser = argparse.ArgumentParser(description='BBC & RAI Radio Player - Player for the British and Italian public broadcasters')
        parser.add_argument('-p', '--player', default='vlc')
        parser.add_argument('player_args', nargs='*')
        args = parser.parse_args()
        self.player_prog = args.player
        self.player_args = args.player_args
        # UI
        self.setWindowTitle(WIN_TITLE)
        self.setMinimumSize(500, 600)
        self.scroll_area = QScrollArea()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)
        self.setCentralWidget(self.scroll_area)
        for name, url in BBC_STATIONS:
            button = QPushButton(name.replace('&', '&&'))
            button.args = {
                'name': name,
                'url': url,
            }
            button.clicked.connect(self.listen)
            self.layout.addWidget(button)

        for name, url in RAI_STATIONS:
            button = QPushButton(name.replace('&', '&&'))
            button.args = {
                'name': name,
                'url': url,
            }
            button.clicked.connect(self.listen)
            self.layout.addWidget(button)

        for name, url in SPANISH_STATIONS:
            button = QPushButton(name.replace('&', '&&'))
            button.args = {
                'name': name,
                'url': url,
            }
            button.clicked.connect(self.listen)
            self.layout.addWidget(button)

        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_player)

    def listen(self):
        pressed_button = self.sender()
        for button in self.widget.findChildren(QPushButton):
            if button != pressed_button and not button.isEnabled():
                button.setEnabled(True)
                break
        pressed_button.setEnabled(False)
        # stop the running player instance before starting another one
        if self.player:
            if self.player.poll() is None:
                self.player.terminate()
                self.player.wait()
        cmd = [self.player_prog]
        cmd.extend(self.player_args)
        cmd.append(pressed_button.args['url'])
        if self.player_prog == 'vlc':
            # RAI blocks us based on User Agent
            cmd.append(":http-user-agent='Mozilla/5.0'")
        print(pressed_button.args['name'], "\n", " ".join(cmd))
        try:
            self.player = subprocess.Popen(cmd)
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setText('Couldn\'t launch\n"%s"' % ' '.join(cmd))
            msg_box.setInformativeText(f"{e}")
            msg_box.exec_()
            pressed_button.setEnabled(True)
        self.setWindowTitle('%s - %s' % (pressed_button.args['name'], WIN_TITLE))
        self.timer.start(200)

    def check_player(self):
        if self.player and self.player.poll() is not None:
            # the player has been stopped
            self.player = None
            self.timer.stop()
            self.setWindowTitle(WIN_TITLE)
            for button in self.widget.findChildren(QPushButton):
                if not button.isEnabled():
                    button.setEnabled(True)
                    break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())

