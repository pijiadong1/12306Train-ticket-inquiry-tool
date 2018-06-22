import requests
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

#获取城市缩写
def fun1():
    # 关闭https证书验证警告

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
    # 12306的城市名和城市代码js文件url
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'

    r = requests.get(url, verify=False)

    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = re.findall(pattern, r.text)
    station = dict(result)

    with open('station.txt', 'w', ) as f:
        f.write(str(station))

#构造一个链接
def get_query_url(text):
    fun1()
    f = open("station.txt", "r")
    fs = f.read()

    # 反转k，v形成新的字典
    code_dict = {v: k for k, v in eval(fs).items()}
    '''
    返回调用api的url链接
    '''
    # 解析参数 aggs[0]里是固定字符串：车票查询 用于匹配公众号接口
    args = str(text).split(' ')

    try:
        date = args[0]
        from_station_name = args[1]
        to_station_name = args[2]
        from_station = eval(fs)[from_station_name]
        to_station = eval(fs)[to_station_name]
    except:
        date, from_station, to_station = '--', '--', '--'
        # 将城市名转换为城市代码

    # api url 构造
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)

    return url

#解析返回值
def query_train_info(url):
    f = open("station.txt", "r")
    fs = f.read()

    # 反转k，v形成新的字典
    code_dict = {v: k for k, v in eval(fs).items()}
    '''
    查询火车票信息：
    返回 信息查询列表
    '''

    info_list = []
    try:

        r = requests.get(url, verify=False)

        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']
        info_list = []
        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'

            # 打印查询结果
            # info_list.append(info)
            info = {"车次名称": train_no, "出发站": from_station_name, "终点站": to_station_name, "出发时间": start_time,
                    "到达时间": arrive_time, "总耗时": time_fucked_up, "一等座": first_class_seat, "二等座": second_class_seat,
                    "软卧": soft_sleep, "硬卧": hard_sleep, "硬座": hard_seat, "无座": no_seat}

            info_list.append(info)
        return info_list
    except:
        return "N"

#主函数
def mian(a, b, c):
    z = a + " " + b + " " + c
    return query_train_info(get_query_url(z))


# text="2018-05-28 广州 哈尔滨"
# s= mian('2018-06-18','广州','哈尔滨')
# print("***********")
# print(s)
# print("***********")
# print(mian(text))