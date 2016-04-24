#  -*- coding: utf-8 -*-
from pyquery import PyQuery

v_source = PyQuery(url='http://yunvs.com/list/mai_1.html')
for data in v_source('tr'):
    v_code = PyQuery(data).find('td').eq(0).text()
    v_name = PyQuery(data).find('td').eq(1).text()
    v_ind = PyQuery(data).find('td').eq(5)
    for i in range(len(PyQuery(v_ind).find('a'))):
        v_indname = PyQuery(v_ind).find('a').eq(i).text()
        print v_code
        print v_name
        print v_indname
