#  -*- coding: utf-8 -*-
from pyquery import PyQuery as PyQ

d = PyQ("http://www.ximalaya.com/dq/all/")
for sort_list in [x.text for x in d('#discoverAlbum .sort_list li a') if d(x).parent().attr('cid') != '0']:
    print sort_list
