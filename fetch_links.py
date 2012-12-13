#!/usr/bin/env python

import mechanize
from pyquery import PyQuery # tested with 1.2.4


br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100214 Gentoo Firefox/3.6')]
response = br.open('http://blog.scoopz.com/2011/05/05/listen-to-any-bbc-radio-live-stream-using-vlc-including-radio-1-and-1xtra/')
d = PyQuery(response.get_data())
for tr in d('table tr').items():
    td_list = tr.find('td')
    if td_list.length:
        name = td_list.eq(0).text()
        link = td_list.eq(1).find('a').attr.href
        print '[%r, %r],' % (name, link)
