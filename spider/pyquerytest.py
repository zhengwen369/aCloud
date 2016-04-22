#  -*- coding: utf-8 -*-
from pyquery import PyQuery as pq

v_source = pq(url='http://yunvs.com/list/mai_1.html')
for data in v_source('tr'):
    v_code = pq(data).find('td').eq(0).text()
    v_name = pq(data).find('td').eq(1).text()
    v_ind = pq(data).find('td').eq(5)
    for i in range(len(pq(v_ind).find('a'))):
        v_indname = pq(v_ind).find('a').eq(i).text()
        print v_code
        print v_name
        print v_indname