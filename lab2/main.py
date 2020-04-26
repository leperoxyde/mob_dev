#!/usr/bin/python
# -*- coding: utf-8 -*-

import pylab
from matplotlib import mlab
import re
import collections


def get_ms(time):
    timepattern = r"[:.]"
    splited = re.split(timepattern, time)
    return int(splited[0]) * 60 * 60 * 1000 + int(splited[1]) * 60 * 1000 + int(splited[2]) * 1000 + int(splited[3])


def tarificate_net(target):
    free_mb = 1000.0 / 1024

    xlist = []
    ylist = []
    data = dict()
    data_file_path = './nf_decoded'
    factor = 1

    data_file = open(data_file_path, 'r')
    cost = 0

    for line in data_file.readlines():
        endpoint = len(line)
        i = 0
        while i < endpoint:
            if (line[i] == ' ' and line[i + 1] == ' '):
                line = line[:i] + line[i + 1:]
                endpoint -= 1
            else:
                i += 1
        linedata = line.split(' ')
        if (target in [linedata[6].split(':')[0], linedata[4].split(':')[0]]):
            data.update({get_ms(linedata[1]): (float(linedata[8]) / 1024 / 1024)})
            cost += factor * (float(linedata[8]) / 1024 / 1024)
    sorted_data = collections.OrderedDict(sorted(data.items()))
    for key, value in sorted_data.items():
        xlist.append(key)
        ylist.append(value)
    xlist.sort()
    pylab.plot(xlist, ylist)
    pylab.savefig('./graph')
    cost -= free_mb * factor
    if cost < 0:
        cost = 0
    return cost


print('Стоимость услуг интернет: ' + str(tarificate_net('217.15.20.194')))
