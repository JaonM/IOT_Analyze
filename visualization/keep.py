# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as pltoff
import re
import os
import time
from analyze.analyze import load_data


def draw_picture(date):
    # output_path = re.match(r'(.*//)(.*)', input_path).group(1) + time.strftime("%Y-%m-%d",time.localtime())
    # + 'picture//'
    # output_path = '../' + time.strftime("%Y-%m-%d", time.localtime()) + '/'
    output_path = '../' + date + '/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    print(output_path)
    # 保存图片所需权限
    # py.sign_in('DemoAccount', '2qdyfjyr7o')
    py.sign_in('templarz', 'PtKMjV9gAzINZqmQRU4T')

    # data = pd.read_excel(file_path)
    data = load_data(date)
    data['times'] = pd.to_datetime(data['获取时间'])
    data = data.sort_values('times')
    data.index = data['times']

    data = data[date]
    # print(data.head(10))

    for s in data['eui'].unique():
        print(s)
        data_list = []
        sensor_data = data[data['eui'] == s]
        if len(sensor_data['温度']) > 0:
            tr_temperature = go.Scatter(
                x=sensor_data['times'],
                y=sensor_data['温度'], name='温度')
            data_list.append(tr_temperature)

        if len(sensor_data['湿度']) > 0:
            tr_humidity = go.Scatter(
                x=sensor_data['times'],
                y=sensor_data['湿度'],
                name='湿度')
            data_list.append(tr_humidity)

        if len(sensor_data['电量']) > 0:
            tr_battery_power = go.Scatter(
                x=sensor_data['times'],
                y=sensor_data['电量'],
                name='电池电量')
            data_list.append(tr_battery_power)
        if len(sensor_data['电流']) > 0:
            tr_current = go.Scatter(x=sensor_data['times'], y=sensor_data['电流'], name='电流')
            data_list.append(tr_current)

        if len(sensor_data['电压']) > 0:
            tr_voltage = go.Scatter(x=sensor_data['times'], y=sensor_data['电压'], name='电压')
            data_list.append(tr_voltage)

        if len(sensor_data['功率']) > 0:
            tr_power = go.Scatter(x=sensor_data['times'], y=sensor_data['功率'], name='功率')
            data_list.append(tr_power)
        # 画图配置
        title_name = str(s)
        layout = go.Layout(title=title_name,
                           margin=go.Margin(
                               l=50,
                               r=0,
                               b=150,
                               t=100,
                               pad=4
                           ),
                           xaxis={'title': '时间', 'zeroline': False},
                           yaxis={'zeroline': False})
        fig = go.Figure(data=data_list, layout=layout)
        # 保存图片
        py.image.save_as(fig, filename=output_path + str(s) + ".png")
        # 生成离线html, 如果图片不好看可以去html缩放到合适
        # pltoff.plot(fig, filename=str(s)+".html" )


# draw_picture(date='2018-01-26')
