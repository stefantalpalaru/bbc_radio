#!/usr/bin/env python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from pprint import pprint
import subprocess
import argparse

# URL list taken from http://blog.scoopz.com/2011/05/05/listen-to-any-bbc-radio-live-stream-using-vlc-including-radio-1-and-1xtra/
STATIONS = [
    ['Radio 1', 'http://bbc.co.uk/radio/listen/live/r1.asx'],
    ['Radio 1Xtra', 'http://bbc.co.uk/radio/listen/live/r1x.asx'],
    ['Radio 2', 'http://bbc.co.uk/radio/listen/live/r2.asx'],
    ['Radio 3', 'http://bbc.co.uk/radio/listen/live/r3.asx'],
    ['Radio 4', 'http://bbc.co.uk/radio/listen/live/r4.asx'],
    ['Radio 4Xtra', 'http://bbc.co.uk/radio/listen/live/r4x.asx'],
    ['Radio 5 Live', 'http://bbc.co.uk/radio/listen/live/r5l.asx'],
    ['Radio 5 Live Sports Extra', 'http://bbc.co.uk/radio/listen/live/r5lsp.asx'],
    ['Radio 6', 'http://bbc.co.uk/radio/listen/live/r6.asx'],
    ['Radio Asian', 'http://bbc.co.uk/radio/listen/live/ran.asx'],
    ['Radio Cymru', 'http://bbc.co.uk/radio/listen/live/rc.asx'],
    ['Radio Foyle', 'http://bbc.co.uk/radio/listen/live/rf.asx'],
    ['Radio nan Gaidheal', 'http://bbc.co.uk/radio/listen/live/rng.asx'],
    ['Radio Scotland', 'http://bbc.co.uk/radio/listen/live/rs.asx'],
    ['Radio Ulster', 'http://bbc.co.uk/radio/listen/live/ru.asx'],
    ['Radio Wales', 'http://bbc.co.uk/radio/listen/live/rw.asx'],
    ['BBC Berkshire', 'http://bbc.co.uk/radio/listen/live/bbcberkshire.asx'],
    ['BBC Bristol', 'http://bbc.co.uk/radio/listen/live/bbcbristol.asx'],
    ['BBC Cambridgeshire', 'http://bbc.co.uk/radio/listen/live/bbccambridgeshire.asx'],
    ['BBC Cornwall', 'http://bbc.co.uk/radio/listen/live/bbccornwall.asx'],
    ['BBC Coventry & Warwickshire', 'http://bbc.co.uk/radio/listen/live/bbccoventryandwarwickshire.asx'],
    ['BBC Cumbria', 'http://bbc.co.uk/radio/listen/live/bbccumbria.asx'],
    ['BBC Derby', 'http://bbc.co.uk/radio/listen/live/bbcderby.asx'],
    ['BBC Devon', 'http://bbc.co.uk/radio/listen/live/bbcdevon.asx'],
    ['BBC Essex', 'http://bbc.co.uk/radio/listen/live/bbcessex.asx'],
    ['BBC Gloucestershire', 'http://bbc.co.uk/radio/listen/live/bbcgloucestershire.asx'],
    ['BBC Guernsey', 'http://bbc.co.uk/radio/listen/live/bbcguernsey.asx'],
    ['BBC Hereford & Worcester', 'http://bbc.co.uk/radio/listen/live/bbcherefordandworcester.asx'],
    ['BBC Humberside', 'http://bbc.co.uk/radio/listen/live/bbchumberside.asx'],
    ['BBC Jersey', 'http://bbc.co.uk/radio/listen/live/bbcjersey.asx'],
    ['BBC Kent', 'http://bbc.co.uk/radio/listen/live/bbckent.asx'],
    ['BBC Lancashire', 'http://bbc.co.uk/radio/listen/live/bbclancashire.asx'],
    ['BBC Leeds', 'http://bbc.co.uk/radio/listen/live/bbcleeds.asx'],
    ['BBC Leicester', 'http://bbc.co.uk/radio/listen/live/bbcleicester.asx'],
    ['BBC Lincolnshire', 'http://bbc.co.uk/radio/listen/live/bbclincolnshire.asx'],
    ['BBC London', 'http://bbc.co.uk/radio/listen/live/bbclondon.asx'],
    ['BBC Manchester', 'http://bbc.co.uk/radio/listen/live/bbcmanchester.asx'],
    ['BBC Merseyside', 'http://bbc.co.uk/radio/listen/live/bbcmerseyside.asx'],
    ['BBC Newcastle', 'http://bbc.co.uk/radio/listen/live/bbcnewcastle.asx'],
    ['BBC Norfolk', 'http://bbc.co.uk/radio/listen/live/bbcnorfolk.asx'],
    ['BBC Northampton', 'http://bbc.co.uk/radio/listen/live/bbcnorthampton.asx'],
    ['BBC Nottingham', 'http://bbc.co.uk/radio/listen/live/bbcnottingham.asx'],
    ['BBC Oxford', 'http://bbc.co.uk/radio/listen/live/bbcoxford.asx'],
    ['BBC Sheffield', 'http://bbc.co.uk/radio/listen/live/bbcsheffield.asx'],
    ['BBC Shropshire', 'http://bbc.co.uk/radio/listen/live/bbcshropshire.asx'],
    ['BBC Solent', 'http://bbc.co.uk/radio/listen/live/bbcsolent.asx'],
    ['BBC Somerset', 'http://bbc.co.uk/radio/listen/live/bbcsomerset.asx'],
    ['BBC Stoke', 'http://bbc.co.uk/radio/listen/live/bbcstoke.asx'],
    ['BBC Suffolk', 'http://bbc.co.uk/radio/listen/live/bbcsuffolk.asx'],
    ['BBC Surrey', 'http://bbc.co.uk/radio/listen/live/bbcsurrey.asx'],
    ['BBC Sussex', 'http://bbc.co.uk/radio/listen/live/bbcsussex.asx'],
    ['BBC Tees', 'http://bbc.co.uk/radio/listen/live/bbctees.asx'],
    ['BBC Three Counties', 'http://bbc.co.uk/radio/listen/live/bbcthreecounties.asx'],
    ['BBC Wiltshire', 'http://bbc.co.uk/radio/listen/live/bbcwiltshire.asx'],
    ['BBC WM', 'http://bbc.co.uk/radio/listen/live/bbcwm.asx'],
    ['BBC York', 'http://bbc.co.uk/radio/listen/live/bbcyork.asx'],
]
WIN_TITLE = "BBC radio"

class Win(QMainWindow):
    def __init__(self, parent=None):
        super(Win, self).__init__(parent)
        self.player = None
        # args
        parser = argparse.ArgumentParser(description='BBC radio player')
        parser.add_argument('-p', '--player', default='vlc')
        parser.add_argument('player_args', nargs='*')
        args = parser.parse_args()
        self.player_prog = args.player
        self.player_args = args.player_args
        # UI
        self.setWindowTitle(WIN_TITLE)
        self.setMinimumSize(300, 600)
        self.scroll_area = QScrollArea()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)
        self.setCentralWidget(self.scroll_area)
        for name, url in STATIONS:
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
        except Exception, e:
            msg_box = QMessageBox()
            msg_box.setText('Couldn\'t launch\n"%s"' % ' '.join(cmd))
            msg_box.setInformativeText(unicode(e))
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

