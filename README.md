bbc\_radio.py is a simple script written in Python and Qt (using the [PySide][0] bindings). It was tested with python-2.7.3 and pyside-1.1.2 .

bbc\_radio.py uses VLC by default but you can specify another player along with some arguments for it like this:

`./bbc_radio.py -p mplayer -- -cache 60 -cache-min 20 -playlist`

Since you'd be doing this from a terminal emulator remember to quit mplayer before closing the bbc\_radio.py window (bbc\_radio.py will leave the player running upon exit, by design).

You might need a nightly VLC build for some MPEG-DASH streams (those ending in .mpd).

[0]: http://qt-project.org/wiki/PySide
