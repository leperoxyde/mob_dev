#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

def tarificate(income_cost = 1, outcome_cost = 3, sms_cost = 1, data_file_path = './data.csv'):

    data_file = open(data_file_path, 'r')
    reader = csv.DictReader(data_file, delimiter=',')

    # Подсчет стоимости телефонных звонков

    cost = 0
    number = '968247916'

    for line in reader:
        call_duration = float(line['call_duration'])

        if ( line['msisdn_origin'] == number ):
            cost+=call_duration*outcome_cost

        if ( line['msisdn_dest'] == number ):
            cost+=call_duration*income_cost

    print('Стоимость звонков: ' + str(cost))

    data_file = open(data_file_path, 'r')
    reader = csv.DictReader(data_file, delimiter=',')

    # Подсчет стоимости SMS

    cost = 0

    for line in reader:
        if ( line['msisdn_origin'] == number ):
            cost += sms_cost*int(line['sms_number'])

    data_file.close()

    print('Стоимость SMS : ' + str(cost))

tarificate()
