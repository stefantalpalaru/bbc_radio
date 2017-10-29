bbc\_radio.py and rai\_radio.py are simple Internet radio scripts written in Python and Qt (using the [PyQt5][0] bindings). They were tested with python-2.7.14 and PyQt5-5.9 .

Both use VLC by default but you can specify another player along with some arguments for it like this:

`./bbc_radio.py -p mplayer -- -cache 60 -cache-min 20 -playlist`

Since you'd be doing this from a terminal emulator remember to quit mplayer before closing the bbc\_radio.py window (bbc\_radio.py will leave the player running upon exit, by design).

You might need a nightly VLC build for some MPEG-DASH streams (those ending in .mpd).

[0]: https://www.riverbankcomputing.com/software/pyqt/intro

