# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as pltoff
import re
import os
import time


def draw_picture(input_path, date):
    output_path = '../' + date + '/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    print(output_path)
    # 保存图片所需权限
    # py.sign_in('DemoAccount', '2qdyfjyr7o')
    py.sign_in('templarz', 'PtKMjV9gAzINZqmQRU4T')

    data = pd.read_excel(input_path)
    data['times'] = pd.to_datetime(data['获取时间'])
    data = data.sort_values('times')
    print(data.head(10))

    for s in data['eui'].unique():
        print(s)
        data_list = []
        sensor_data = data[data['eui'] == s]
        tr_temperature = go.Scatter(
            x=sensor_data['获取时间'],
            y=sensor_data['温度'],
            name='温度')
        tr_humidity = go.Scatter(
            x=sensor_data['获取时间'],
            y=sensor_data['湿度'],
            name='湿度')
        tr_battery_power = go.Scatter(
            x=sensor_data['获取时间'],
            y=sensor_data['电量'],
            name='电池电量')
        data_list.append(tr_temperature)
        data_list.append(tr_humidity)
        data_list.append(tr_battery_power)
        # 画图配置
        title_name = s
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


draw_picture("../input/2018-01-24.xlsx", '2018-01-24')
