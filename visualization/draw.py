# -*- coding:utf-8 -*-
import pandas as pd
import re
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import matplotlib as mpl
import os
import numpy as np

mpl.rcParams['font.sans-serif'] = u'Microsoft YaHei'  # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

input_path = 'C://Users//lenovo//Desktop//IOT_Analyze//IOT_Analyze//input//'


def draw(file_name, date_range=None, save_folder=str(datetime.datetime.now().date())):
    """

    :param file_name:
    :param date_range: list/array ['yyyy-mm-dd',...]
    :return:
    """
    if re.search('.csv', file_name):
        data = pd.read_csv(input_path + file_name)
    elif re.search('.xlsx', file_name):
        data = pd.read_excel(input_path + file_name)
    else:
        print("invalid file format")
        return
    data['times'] = pd.to_datetime(data['获取时间'])
    data['temperature'] = data['温度']
    data['humidity'] = data['湿度']
    data['power'] = data['功率']
    data['current'] = data['电流']
    data['voltage'] = data['电压']
    data.index = pd.to_datetime(data['获取时间'])

    # os.rmdir('../'+save_folder)
    # os.removedirs('../'+save_folder)
    # os.mkdir('../' + save_folder)
    for s in data['传感器名称'].unique():
        print(str(s))
        sensor = data[data['传感器名称'] == s]
        for date in date_range:
            try:
                sub_sensor = sensor[date]
            except KeyError:
                print('loss current date data date: ' + date)
                continue
            # 每3采样一个
            sub_sensor = sub_sensor[::3]
            time = sub_sensor['times'].values[::10]
            time = pd.DatetimeIndex(time)
            t = time.map(lambda x: x.time())
            # t = t.map(lambda x: str(x))
            # t = np.array(t)
            # # time = datetime.datetime(time.time)
            # # time = time.map(lambda x:str(x))
            # # time = time.map(lambda x: datetime.datetime(x))
            # print(t)
            if len(sub_sensor['传感器名称']) > 0:
                try:
                    sub_sensor.plot(y=['temperature', 'humidity', 'power', 'voltage', 'current'], x='获取时间',
                                    subplots=True, figsize=(12, 8), title=str(sub_sensor['eui'][0]) + ' ' + s)
                    # fig = ax[0].get_figure()
                    # fig.savefig(date + ' ' + str(eui) + ' ' +
                    #             sub_sensor['传感器名称'][0] + '.jpg')
                    plt.savefig(
                        '../' + save_folder + '/' + date + ' ' + str(sub_sensor['eui'][0]) + ' ' + s + '.png')
                except TypeError:
                    print('empty dataframe')
            elif len(sub_sensor['eui']) > 0:
                try:
                    print(sub_sensor)
                    sub_sensor.plot(y=['temperature', 'humidity', 'power', 'voltage', 'current'], x='times',
                                    subplots=True, figsize=(12, 8), title=str(sub_sensor['eui'][0]))
                    # fig = ax[0].get_figure()
                    # fig.savefig(date + ' ' + str(eui) + '.jpg')
                    plt.savefig('../' + save_folder + '/' + date + ' ' + str(sub_sensor['eui'][0]) + '.png')
                except TypeError:
                    print('empty dataframe')
                    # sensor1 = data[data['eui'] == 9896830000000010]
                    # sub_sensor1 = sensor1['2018-01-06']

                    # plt.show()


# draw('data_201801081649_1.xlsx', ['2018-01-06', '2018-01-07', '2018-01-08'])

draw('2018-1-9.xlsx', ['2018-01-09'])
