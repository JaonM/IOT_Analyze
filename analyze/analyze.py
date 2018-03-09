# -*- coding:utf-8 -*-

import pandas as pd
import datetime
import numpy as np
import MySQLdb
import math
from analyze.hotel_sensor_config import sensor_config

input_path = '../input/'


def load_data(date):
    db = MySQLdb.connect(host='218.17.171.90',
                         user='dingzhiwen',
                         passwd='Dzw@123456',
                         db='siat_iot')
    cursor = db.cursor()
    cursor.execute("select tb2.eui,tb2.temperature 温度,tb2.humidity 湿度, tb2.batt 电量,tb2.current 电流,tb2.voltage 电压,tb2.power 功率,tb2.ts 获取时间,tb1.name 传感器名称,tb3.name 所属设备,tb4.name 所属酒店\
                            from tb_sensor_data tb2 LEFT JOIN tb_sensor tb1 on tb1.code = tb2.eui LEFT JOIN tb_equipment tb3 on tb3.equipment_id = tb1.equipment_id \
                            LEFT JOIN tb_customer tb4 on tb4.customer_id = tb1.customer_id where (tb2.eui='9896830000000008' or tb2.eui='9896830000000002' or tb2.eui = '9896830000000003' \
                             or tb2.eui='9896830000000004' or tb2.eui = '9896830000000006' or tb2.eui = '3786E6ED0034004B' or \
                             tb2.eui = '3768B26900230053' or tb2.eui = '4768B269002B0059' or tb2.eui = '4768B269001F003F' or \
                             tb2.eui='4778B269003B002F' or tb2.eui='3430363057376506' or tb2.eui='3430363067378B07' or tb2.eui = '3430363064378607' \
                             or tb2.eui='343036305D375E05' or tb2.eui = '3430363064378007') and tb2.ts >" + date + " ORDER BY ts asc")
    results = []
    for row in cursor.fetchall():
        results.append(
            {'eui': row[0], '温度': row[1], '湿度': row[2], '电量': row[3], '电流': row[4], '电压': row[5], '功率': row[6],
             '获取时间': row[7], '传感器名称': row[8], '所属设备': row[9], '所属酒店': row[10]})
    df = pd.DataFrame(data=results)
    return df


# def load_data(start_date, end_date):
#     db = MySQLdb.connect(host='218.17.171.90',
#                          user='dingzhiwen',
#                          passwd='Dzw@123456',
#                          db='siat_iot')
#     cursor = db.cursor()
#     cursor.execute("select tb2.eui,tb2.temperature 温度,tb2.humidity 湿度, tb2.batt 电量,tb2.current 电流,tb2.voltage 电压,tb2.power 功率,tb2.ts 获取时间,tb1.name 传感器名称,tb3.name 所属设备,tb4.name 所属酒店\
#                             from tb_sensor_data tb2 LEFT JOIN tb_sensor tb1 on tb1.code = tb2.eui LEFT JOIN tb_equipment tb3 on tb3.equipment_id = tb1.equipment_id \
#                             LEFT JOIN tb_customer tb4 on tb4.customer_id = tb1.customer_id where (tb2.eui = '9896830000000003' or \
#                            tb2.eui = '4768B269002B0059') and tb2.ts >" + start_date + " and tb2.ts <" + end_date + " ORDER BY ts desc")
#     results = []
#     for row in cursor.fetchall():
#         results.append(
#             {'eui': row[0], '温度': row[1], '湿度': row[2], '电量': row[3], '电流': row[4], '电压': row[5], '功率': row[6],
#              '获取时间': row[7], '传感器名称': row[8], '所属设备': row[9], '所属酒店': row[10]})
#     df = pd.DataFrame(data=results)
#     print(df.head())
#     return df


def threshold_load():
    threshold = {'9896830000000008': {'mintemperature': -22, 'maxtemperature': -10},
                 '9896830000000002': {'mintemperature': -22, 'maxtemperature': -10},
                 '9896830000000003': {'mintemperature': 0, 'maxtemperature': 10},
                 '9896830000000004': {'mintemperature': 2, 'maxtemperature': 10},
                 '9896830000000006': {'mintemperature': -22, 'maxtemperature': -10},
                 '3786E6ED0034004B': {'mintemperature': -22, 'maxtemperature': -10},
                 '3768B26900230053': {'mintemperature': -22, 'maxtemperature': -10},
                 '4768B269002B0059': {'mintemperature': 0, 'maxtemperature': 10},
                 '4768B269001F003F': {'mintemperature': 2, 'maxtemperature': 10},
                 '4778B269003B002F': {'mintemperature': -22, 'maxtemperature': 10}}
    return threshold


def load_threshold(file_name='03-09.xlsx'):
    """

    :param file_name: history data file
    :return: a dict with sensors and their threshold
    """
    if file_name is None:
        print("file name must not be none quit.....")

    print('loading data...')
    df_base = pd.read_excel(input_path + file_name)
    result = dict()

    for sensor_name in df_base['传感器名称'].unique():
        sensor = df_base[df_base['传感器名称'] == sensor_name]
        # print(sensor['温度'].describe())
        result[sensor_name] = {'mintemperature': sensor['温度'].describe()['min'],
                               'maxtemperature': sensor['温度'].describe()['max'],
                               'minhumidity': sensor['湿度'].describe()['min'],
                               'maxhumidity': sensor['湿度'].describe()['max'],
                               'minbatt': sensor['电量'].describe()['min'],
                               'maxbatt': sensor['电量'].describe()['max'],
                               'mincurrent': sensor['电流'].describe()['min'],
                               'maxcurrent': sensor['电流'].describe()['max'],
                               'minvoltage': sensor['电压'].describe()['min'],
                               'maxvoltage': sensor['电压'].describe()['max'],
                               'minpower': sensor['功率'].describe()['min'],
                               'maxpower': sensor['功率'].describe()['max']}
    result['温湿度传感器1']['minhumidity'] = 0
    result['温湿度传感器1']['maxhumidity'] = 100
    result['温湿度传感器3']['minhumidity'] = 0
    result['温湿度传感器3']['maxhumidity'] = 100
    result['温湿度传感器4']['minhumidity'] = 0
    result['温湿度传感器4']['maxhumidity'] = 100

    df_requirement = pd.read_excel(input_path + '要求范围.xlsx')
    for index, item in df_requirement.iterrows():
        try:
            result[item['name']]['eui'] = item['code']
            result[item['name']]['is_base'] = item['isbase']
        except KeyError:
            continue

    return result


err_code = {0: 'normal', 1: 'error', -1: 'missing'}


def analyze_data(threshold_file='03-09.xlsx', date=datetime.datetime.now().date().strftime('%Y-%m-%d')):
    """
    err_code:   0 normal    1 error -1 missing

    :param file_name:
    :param threshold_file:
    :param date:
    :return:
    """
    # if file_name is None:
    #     print('file name can not be none...quiting...')
    # df = pd.read_excel(input_path + file_name)
    # threshold = load_threshold(threshold_file)
    df = load_data(date)
    threshold = threshold_load()
    result = dict()
    result['date'] = date
    result['results'] = list()
    df.index = pd.to_datetime(df['获取时间'])
    dimensions = ['温度', '湿度', '电量', '电流', '电压', '功率']
    dimension_threshold_mapping = {'温度': ('mintemperature', 'maxtemperature'), '湿度': ('minhumidity', 'maxhumidity'),
                                   '电量': ('minbatt', 'maxbatt'), '电流': ('mincurrent', 'maxcurrent'),
                                   '电压': ('minvoltage', 'maxvoltage'), '功率': ('minpower', 'maxpower')}

    threshold_dimension = ['温度']  # 需要阈值分析的维度

    # for sensor_name in df['eui'].unique():
    for key in sensor_config.keys():
        for sensor_name in sensor_config[key]:
            sensor = df[df['eui'] == sensor_name['eui']]
            _discrete_loss_times = 0  # 离散丢包次数
            _total_loss_time = 0  # 缺失总时间
            try:
                sensor = sensor[date]
                # sensor = sensor[sensor['获取时间'] > date ]
                # sensor = sensor[sensor['获取时间'] < '2018-02-09' + ' 11:30:00']
                messages = dict()
                err_code = 0
                # handle temperature
                for dimension in dimensions:
                    # print(sensor)
                    data = sensor[dimension]
                    # print(data.values)
                    msg = list()
                    if len(data.values) > 0:
                        # dimension = '温度'
                        basic = data.describe()
                        # print(basic)
                        try:
                            msg.append({'status': 'normal', 'msg': dimension + '平均值为: ' + str(basic['mean']) + ','})
                            msg.append({'status': 'normal', 'msg': dimension + '最小值为: ' + str(basic['min']) + ','})
                            msg.append({'status': 'normal', 'msg': dimension + '最大值为: ' + str(basic['max']) + ','})
                        except KeyError:
                            pass
                        if dimension not in threshold_dimension:
                            messages[dimension] = msg
                            continue
                        try:
                            if basic['min'] < threshold[sensor_name['eui']][dimension_threshold_mapping[dimension][0]]:
                                err_code = 1
                                min_time = sensor[sensor[dimension] == basic['min']]['获取时间']
                                # min_time = min_time.time().strftime('%H:%m:%s')
                                # print(min_time)
                                min_time = min_time.map(lambda x: str(x).split()[1])
                                msg.append({'status': 'red', 'msg': dimension + '最小值低于阈值下限(' + str(
                                    threshold[sensor_name['eui']][
                                        dimension_threshold_mapping[dimension][0]]) + ')，时间为:' + str(
                                    min_time.values) + '\n'})
                            if basic['max'] > threshold[sensor_name['eui']][dimension_threshold_mapping[dimension][1]]:
                                err_code = 1
                                max_time = sensor[sensor[dimension] == basic['max']]['获取时间']
                                # print(max_time.values)
                                max_time = max_time.map(lambda x: str(x).split()[1])
                                # max_time = max_time.time().strftime('%H:%m:%s')
                                # print(max_time.values)
                                msg.append({'status': 'red', 'msg': dimension + '最大值高于阈值上限(' + str(
                                    threshold[sensor_name['eui']][
                                        dimension_threshold_mapping[dimension][1]]) + ')，时间为: ' + str(
                                    max_time.values) + '\n'})
                        except KeyError:
                            pass
                    messages[dimension] = msg

                times = sensor['获取时间']
                times = pd.to_datetime(times)
                msgs = []
                if len(times) > 1:
                    # 获取时间频率判断 平均获取频率 增加首尾时间

                    # second_delta = (times[0] - datetime.datetime.strptime(date, '%Y-%m-%d')).total_seconds()
                    second_delta = 0
                    for i in range(1, len(times)):
                        delta = times[i] - times[i - 1]
                        # print(delta)
                        second_delta += delta.total_seconds()
                        # print(second_delta)
                    # print(len(times))
                    # second_delta += (datetime.datetime.strptime(date + ' 23:59:59', '%Y-%m-%d %H:%M:%S') - times[
                    #     len(times) - 1]).total_seconds()
                    # avg_minutes = (second_delta / (len(times) - 1 + 2)) / 60
                    avg_minutes = (second_delta / (len(times) - 1)) / 60
                    msgs.append(
                        {'status': 'red', 'msg': '\n该设备平均获取时间频率为: ' + str(round(avg_minutes, 3)) + '分钟\n'})

                    # 计算时间方差
                    square_error = 0
                    for i in range(1, len(times)):
                        delta = times[i] - times[i - 1]
                        square_error = square_error + (delta.total_seconds() / 60 - avg_minutes) ** 2
                    square_error = square_error / (len(times) - 1)
                    msgs.append({'status': 'red', 'msg': '\n该设备获取时间方差为: ' + str(square_error) + '\n'})

                    # 计算丢包频率
                    lost_count = 0
                    # 开始丢包时间
                    _start_loss = 0
                    # _end_loss = 1
                    _start_loss_time = 0
                    _end_loss_time = 0
                    _continuous_lost_flag = False  # 是否连续丢包标记符
                    for i in range(0, len(times)):
                        _is_loss_flag = 0  # 是否重复结算连续丢包
                        # print(delta)
                        # second_delta += delta
                        # print(delta.item())
                        if i == 0:
                            delta = times[i] - datetime.datetime.strptime(date, '%Y-%m-%d')
                            if delta.total_seconds() > 6 * sensor_name['frequency']:
                                lost_count += math.ceil(delta.total_seconds() / sensor_name['require_frequency'])
                                '''数据缺失情况'''
                                msgs.append({'status': 'red',
                                             'msg': '缺失数据时间大于' + str(
                                                 math.floor(6 * sensor_name[
                                                     'frequency'] / 60)) + '分钟时间为,' + date + ' 0:00:00' + ',' + times[
                                                        i].strftime('%Y-%m-%d %H:%M:%S') + ',' + str(
                                                 math.floor(delta.total_seconds() / 60)) + ' 分钟,' + str(
                                                 math.ceil(delta.total_seconds() / sensor_name[
                                                     'require_frequency'])) + '次\n'})
                                _total_loss_time += math.floor(delta.total_seconds() / 60)
                                continue
                        else:
                            delta = times[i] - times[i - 1]

                        if delta.total_seconds() > sensor_name['frequency']:

                            if delta.total_seconds() > 6 * sensor_name['frequency']:
                                '''
                                若缺失数据时间段包括丢包时间则先结算丢包时间
                                '''
                                if _start_loss == 1 and _start_loss_time != 0:
                                    _start_loss = 0
                                    time_diff = times[i - 1] - _start_loss_time
                                    msgs.append(
                                        {'status': 'blue',
                                         'msg': '结束丢包时间为, ' + times[i - 1].strftime('%Y-%m-%d %H:%M:%S') + ',' + str(
                                             math.floor(
                                                 time_diff.total_seconds() / sensor_name[
                                                     'require_frequency'])-1) + '次\n'})
                                    _discrete_loss_times += math.floor(
                                        time_diff.total_seconds() / sensor_name['require_frequency']) - 1
                                lost_count += math.ceil(delta.total_seconds() / sensor_name['require_frequency'])

                                '''数据缺失情况'''
                                msgs.append({'status': 'red',
                                             'msg': '缺失数据时间大于' + str(
                                                 math.floor(6 * sensor_name['frequency'] / 60)) + '分钟时间为,' + times[
                                                        i - 1].strftime(
                                                 '%Y-%m-%d %H:%M:%S') + ',' + times[i].strftime(
                                                 '%Y-%m-%d %H:%M:%S') + ',' + str(
                                                 math.floor(delta.total_seconds() / 60)) + ' 分钟,' + str(math.ceil(
                                                 delta.total_seconds() / sensor_name['require_frequency'])) + '次\n'})
                                _total_loss_time += math.floor(delta.total_seconds() / 60)
                                continue
                            # lost_count += 1

                            # _start_loss = 0
                            if _start_loss == 0:
                                _start_loss = 1
                                _start_loss_time = times[i - 1]
                                _count = i
                                msgs.append(
                                    {'status': 'blue',
                                     'msg': '开始丢包时间为, ' + times[i - 1].strftime('%Y-%m-%d %H:%M:%S') + ','})
                        elif delta.total_seconds() <= sensor_name['frequency']:
                            # _end_loss=1
                            if _start_loss == 1:
                                _start_loss = 0
                                _end_loss_time = times[i - 1]
                                _is_loss_flag = 1
                                _count = i - _count
                                time_diff = _end_loss_time - _start_loss_time
                                lost_count += math.ceil(
                                    time_diff.total_seconds() / sensor_name['require_frequency'] - 1)
                                _discrete_loss_times += math.floor(
                                    time_diff.total_seconds() / sensor_name['require_frequency'] - 1)
                                msgs.append(
                                    {'status': 'blue',
                                     'msg': '结束丢包时间为, ' + times[i - 1].strftime('%Y-%m-%d %H:%M:%S') + ',' + str(
                                         math.floor(
                                             time_diff.total_seconds() / sensor_name[
                                                 'require_frequency']) - 1) + '次\n'})
                        # print(_end_loss_time)
                        # print(_start_loss_time)
                        if _end_loss_time is not 0 and _start_loss_time is not 0 and _is_loss_flag == 1:
                            time_diff = _end_loss_time - _start_loss_time
                            # print(time_diff)
                            if time_diff.total_seconds() > 6 * sensor_name['frequency']:
                                _is_loss_flag = 0
                                _continuous_lost_flag = True
                                msgs.append(
                                    {'status': 'normal',
                                     'msg': '持续丢包大于' + str(math.floor(
                                         6 * sensor_name['frequency'] / 60)) + '分钟 丢包周期为,' + _start_loss_time.strftime(
                                         '%Y-%m-%d %H:%M:%S') + ' , ' + _end_loss_time.strftime(
                                         '%Y-%m-%d %H:%M:%S') + ', ' + str(math.floor(
                                         time_diff.total_seconds() / sensor_name['frequency'])) + '次,' + str(
                                         _count - 1) + '次' + '\n'
                                     })

                        # square_error = square_error + (delta.total_seconds() / 60 - avg_minutes) ** 2
                    # square_error = square_error / (len(times) - 1)

                    if not _continuous_lost_flag and lost_count != 0:
                        '''
                        没有连续丢包的情况
                        '''
                        # msgs.append({'status': 'red', 'msg': '虽有数次丢包，但是均为离散丢包，没有丢包持续时间超过30分钟的情况。\n'})

                    # msgs.append({'status': 'red', 'msg': '该设备获取时间方差为: ' + str(square_error) + '\n'})

                    '''与获取时间点相比计算缺失情况'''
                    now = datetime.datetime.now()
                    if now < datetime.datetime.strptime(date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'):
                        delta = now - times[-1]
                        if delta.total_seconds() > 6 * sensor_name['frequency']:
                            lost_count += math.ceil(delta.total_seconds() / sensor_name['require_frequency'])
                            msgs.append({'status': 'red',
                                         'msg': '缺失数据时间大于' + str(
                                             math.floor(6 * sensor_name['frequency'] / 60)) + '分钟时间为,' + times[
                                                    -1].strftime('%Y-%m-%d %H:%M:%S') + ',' + now.strftime(
                                             '%Y-%m-%d %H:%M:%S') + ',' + str(
                                             math.floor(delta.total_seconds() / 60)) + ' 分钟,' + str(math.ceil(
                                             delta.total_seconds() / sensor_name['require_frequency'])) + '次\n'})
                            _total_loss_time += math.floor(delta.total_seconds() / 60)

                    else:
                        now = datetime.datetime.strptime(date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
                        delta = now - times[-1]
                        if delta.total_seconds() > 6 * sensor_name['frequency']:
                            lost_count += math.ceil(delta.total_seconds() / sensor_name['require_frequency'])
                            _total_loss_time += math.floor(delta.total_seconds() / 60)
                            # msgs.append({'status': 'red',
                            #              'msg': '缺失数据时间大于' + str(
                            #                  math.floor(6 * sensor_name['frequency'] / 60)) + '分钟时间为,' + times[
                            #                         -1].strftime(
                            #                  '%Y-%m-%d %H:%M:%S') + ',' + date + ' 23:59:59' + ',' + str(
                            #                  math.floor(delta.total_seconds() / 60)) + ' 分钟,' + str(math.ceil(
                            #                  delta.total_seconds() / sensor_name['require_frequency'])) + '次\n'})

                            msgs.append({'status': 'red',
                                         'msg': '缺失数据时间大于' + str(
                                             math.floor(6 * sensor_name['frequency'] / 60)) + '分钟时间为,' + times[
                                                    -1].strftime('%Y-%m-%d %H:%M:%S') + ',' + now.strftime(
                                             '%Y-%m-%d %H:%M:%S') + ',' + str(
                                             math.floor(delta.total_seconds() / 60)) + ' 分钟,' + str(math.ceil(
                                             delta.total_seconds() / sensor_name['require_frequency'])) + '次\n'})

                    '''计算丢包率'''
                    # msgs.append({'status': 'red',
                    #              'msg': '该设备丢包次数为: ' + str(lost_count) + '/' + str(math.ceil(
                    #                  (now - datetime.datetime.strptime(date + ' 0:00:00',
                    #                                                    '%Y-%m-%d %H:%M:%S')).total_seconds() /
                    #                  sensor_name['require_frequency'])) + ',丢包率为: ' + str(round(lost_count / (math.ceil(
                    #                  (now - datetime.datetime.strptime(date + ' 0:00:00',
                    #                                                    '%Y-%m-%d %H:%M:%S')).total_seconds() /
                    #                  sensor_name['require_frequency'])), 4)) + '\n'})
                    suppose_count = math.ceil(
                        (now - datetime.datetime.strptime(date + ' 0:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds() /
                        sensor_name['require_frequency'])
                    if suppose_count < len(times):
                        suppose_count = len(times)
                    msgs.append({'status': 'red',
                                 'msg': '该设备接收记录次数为: ' + str(len(times)) + '/' + str(suppose_count) + ',丢包率为: ' + str(
                                     round((suppose_count - len(times)) / suppose_count, 4)) + '\n'})
                    # msgs.append({'status': 'red',
                    #              'msg': '该设备丢包记录次数为: ' + str(lost_count) + '/' + str(suppose_count) + ',丢包率为: ' + str(
                    #                  round(lost_count / suppose_count, 4))+'\n'})
                    msgs.append({'status': 'red',
                                 'msg': '离散丢包次数为: ' + str(_discrete_loss_times) + ',缺失时间总共为: ' + str(
                                     _total_loss_time) + '分钟'})

                else:
                    msgs.append({'status': 'red', 'msg': '数据丢失'})
                messages['时间频率'] = msgs

                try:
                    result['results'].append(
                        {'eui': sensor_name['eui'], 'info': '有分析结果', 'err_code': err_code, 'is_base':
                            threshold[sensor_name['eui']]['is_base'], 'messages': messages, 'company': key})
                except KeyError:
                    result['results'].append(
                        {'eui': sensor_name['eui'], 'info': '有分析结果', 'err_code': err_code, 'is_base': 0,
                         'messages': messages, 'company': key})

            except KeyError:
                try:
                    result['results'].append({'eui': sensor_name['eui'], 'info': '缺失当天数据\n', 'err_code': -1,
                                              'is_base': threshold[sensor_name['eui']]['is_base'],
                                              'company': key})
                except KeyError:
                    result['results'].append({'eui': sensor_name['eui'], 'info': '缺失当天数据\n', 'err_code': -1,
                                              'is_base': 0, 'company': key})
    return result


# print(load_threshold('要求范围.xlsx'))
# print(analyze_data('2018-1-9.xlsx', '要求范围.xlsx', '2018-01-09'))
if __name__ == '__main__':
    # df = load_data('2018-01-26')
    # print(df.head())
    print(analyze_data(date='2018-01-29'))
