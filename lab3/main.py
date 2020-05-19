#!/usr/bin/python
# -*- coding: utf-8 -*-
# lab 3

import csv
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import pdfkit
import pylab
from matplotlib import mlab
import re
import collections


def tarificate(income_cost=1, outcome_cost=3, sms_cost=1, data_file_path='./data.csv'):

    data_file = open(data_file_path, 'r')
    reader = csv.DictReader(data_file, delimiter=',')

    # Подсчет стоимости телефонных звонков

    cost = 0
    number = '968247916'

    for line in reader:
        call_duration = float(line['call_duration'])

        if (line['msisdn_origin'] == number):
            cost += call_duration * outcome_cost

        if (line['msisdn_dest'] == number):
            cost += call_duration * income_cost

    callcost = cost

    data_file = open(data_file_path, 'r')
    reader = csv.DictReader(data_file, delimiter=',')

    # Подсчет стоимости SMS

    cost = 0

    for line in reader:
        if (line['msisdn_origin'] == number):
            cost += sms_cost * int(line['sms_number'])

    data_file.close()

    smscost = cost

    return callcost, smscost


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


def generate_pdf(output, bik, src_num, inn, kpp, dst, number, date, customer, tel, sms, net):

    html_template_file = open('./invoice.html.j2', 'r')
    template = html_template_file.read()
    html_template_file.close()
    env = Environment(loader=FileSystemLoader('.'))
    invoice = env.get_template('invoice.html.j2')
    sum = tel + sms + net
    invoice_content = invoice.render(
        BIK=bik,
        SRC_NUM=src_num,
        INN=inn,
        KPP=kpp,
        DST_NUM=dst,
        NUMBER=number,
        DATE=date,
        CUSTOMER=customer,
        TEL=tel,
        SMS=sms,
        NET=net,
        SUM=sum
    )

    invoice_html = open('tmp_html.html', 'w')
    invoice_html.write(invoice_content.encode('utf-8'))
    invoice_html.close()
    pdfkit.from_url('./tmp_html.html', output)


counter = tarificate()

tel, sms = tarificate()
net = tarificate_net('217.15.20.194')

generate_pdf(
    './invoice.pdf',
    '123456789',
    '123456789098',
    '987654321',
    '1231231231',
    '12341234123412341',
    '1',
    '26.10.1999',
    u'Винокурцев И. Б.',
    tel,
    sms,
    round(net, 2)
)
