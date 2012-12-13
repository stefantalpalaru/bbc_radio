bbc\_radio.py is a simple script written in python and Qt (using the pyside bindings). It was tested with python-2.7.3 and pyside-1.1.2 .

For educational purposes, this repo includes fetch\_links.py - the script used to scrape the list of radio stations and corresponding links from [blog.scoopz.com][1]. This file is not used by bbc\_radio.py so it should not be installed.

bbc\_radio.py uses VLC by default but you can specify another player along with some arguments for it like this:

`./bbc_radio.py -p mplayer -- -cache 60 -cache-min 20 -playlist`

Since you'd be doing this from a terminal emulator remember to quit mplayer before closing the bbc\_radio.py window (bbc\_radio.py will leave the player running upon exit, by design).

[1]: http://blog.scoopz.com/2011/05/05/listen-to-any-bbc-radio-live-stream-using-vlc-including-radio-1-and-1xtra/
