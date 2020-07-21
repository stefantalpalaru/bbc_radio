#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QPushButton, QMessageBox
#from pprint import pprint
import subprocess
import argparse

# URL list taken from Wikipedia
BBC_STATIONS = [
    ['BBC World Service - English News', 'http://www.bbc.co.uk/worldservice/meta/live/mp3/ennws.pls'],
    ['BBC Radio 1', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_one/format/pls.pls'],
    ['BBC Radio 1Xtra', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_1xtra/format/pls.pls'],
    ['BBC Radio 2', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_two/format/pls.pls'],
    ['BBC Radio 3', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_three/format/pls.pls'],
    ['BBC Radio 4', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_fourfm/format/pls.pls'],
    ['BBC Radio 4Xtra', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_four_extra/format/pls.pls'],
    ['BBC Radio 5 Live', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_five_live/format/pls.pls'],
    ['BBC Radio 5 Live Sports Extra (Geo-Restricted)', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_radio_five_live_sports_extra/format/pls.pls'],
    ['BBC Radio 6', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_6music/format/pls.pls'],
    ['BBC Asian Network', 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/http-icy-mp3-a/vpid/bbc_asian_network/format/pls.pls'],
    ['BBC Radio Scotland', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_scotland_fm.mpd'],
    [u'BBC Radio nan Gàidheal', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_nan_gaidheal.mpd'],
    ['BBC Radio Wales', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_wales_fm.mpd'],
    ['BBC Radio Cymru', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_cymru.mpd'],
    ['BBC Radio Ulster', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_ulster.mpd'],
    ['BBC Radio Foyle', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_foyle.mpd'],
    ['BBC Berkshire', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_berkshire.mpd'],
    ['BBC Bristol', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_bristol.mpd'],
    ['BBC Cambridgeshire', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_cambridge.mpd'],
    ['BBC Cornwall', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_cornwall.mpd'],
    ['BBC Coventry & Warwickshire', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_coventry_warwickshire.mpd'],
    ['BBC Cumbria', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_cumbria.mpd'],
    ['BBC Derby', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_derby.mpd'],
    ['BBC Devon', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_devon.mpd'],
    ['BBC Essex', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_essex.mpd'],
    ['BBC Gloucestershire', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_gloucestershire.mpd'],
    ['BBC Guernsey', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_guernsey.mpd'],
    ['BBC Hereford & Worcester', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_hereford_worcester.mpd'],
    ['BBC Humberside', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_humberside.mpd'],
    ['BBC Jersey', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_jersey.mpd'],
    ['BBC Kent', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_kent.mpd'],
    ['BBC Lancashire', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_lancashire.mpd'],
    ['BBC Leeds', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_leeds.mpd'],
    ['BBC Leicester', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_leicester.mpd'],
    ['BBC Lincolnshire', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_lincolnshire.mpd'],
    ['BBC London', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_london.mpd'],
    ['BBC Manchester', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_manchester.mpd'],
    ['BBC Merseyside', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_merseyside.mpd'],
    ['BBC Newcastle', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_newcastle.mpd'],
    ['BBC Norfolk', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_norfolk.mpd'],
    ['BBC Northampton', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_northampton.mpd'],
    ['BBC Nottingham', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_nottingham.mpd'],
    ['BBC Oxford', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_oxford.mpd'],
    ['BBC Sheffield', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_sheffield.mpd'],
    ['BBC Shropshire', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_shropshire.mpd'],
    ['BBC Solent', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_solent.mpd'],
    ['BBC Somerset', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_somerset_sound.mpd'],
    ['BBC Stoke', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_stoke.mpd'],
    ['BBC Suffolk', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_radio_suffolk.mpd'],
    ['BBC Surrey', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_surrey.mpd'],
    ['BBC Sussex', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_sussex.mpd'],
    ['BBC Tees', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_tees.mpd'],
    ['BBC Three Counties', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/ak/bbc_three_counties_radio.mpd'],
    ['BBC Wiltshire', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_radio_wiltshire.mpd'],
    ['BBC WM', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnw/bbc_wm.mpd'],
    ['BBC York', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/aks/bbc_radio_york.mpd'],
    ['BBC World Service - Internet Schedule', 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/sbr_low/llnw/bbc_world_service.m3u8'],
    ['BBC World Service - Africa', 'http://www.bbc.co.uk/worldservice/meta/live/mp3/enafw.pls'],
    ['BBC Arabic Radio', 'https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_arabic_radio.mpd'],
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
    ['RAI Radio Tutta Italia', 'http://icestreaming.rai.it/11.mp3']
]

WIN_TITLE = "BBC & RAI Radio"

class Win(QMainWindow):
    def __init__(self, parent=None):
        super(Win, self).__init__(parent)
        self.player = None
        # args
        parser = argparse.ArgumentParser(description='BBC&RAI Radio Player - Player of the British and Italian public player broadcaster')
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

