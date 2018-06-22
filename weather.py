import requests
from bs4 import BeautifulSoup
import re,time
from weather_id import mylist

#传入时间,最高温度,最低温度列表,天气列表
def show_weather(m,sumht,sumlt,sumwea):
    l = m.split('-')
    s1 = time.strptime('%d %d %d'%(int(l[0]),int(l[1]),int(l[2])),'%Y %m %d')
    s2 = time.localtime(time.time())
    s3 = s1[-2] - s2[-2]
    try:
        l1 = '温度:'+sumlt[s3]+'℃'+' '+'~'+sumht[s3]
        l2 = '天气:'+sumwea[s3]
    except:
        print('未查询到天气!!!')
    else:
        return (l1,l2)

#获取城市的ID
def get_id(name_id):
    l = mylist()
    for i in l:
        if i['name'] == name_id:
            s = i['id']
    return s
#爬取未来七天的天气
def get_7dweather(header,id):
    #最高温
    temperatureHigh = []
    temperatureLow1 = []
    #最低温度
    temperatureLow = []
    #天气
    wth = []
    url = 'http://www.weather.com.cn/weather/%s.shtml'%id
    req = requests.get(url,headers=header)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html,'lxml')
    tagToday = bs.select('p[class="tem"]')
    wth1 = bs.select('p[class="wea"]')
    for x in tagToday:
        try:
            temperatureHigh.append(x.span.string)
        except:
            pass
        else:
            temperatureHigh.append(x.span.string)
    # print(temperatureHigh)
    for y in tagToday:
        temperatureLow1.append(y.i.string)
    # print(temperatureLow1)
    for z in wth1:
        wth.append(z.string)
    # print(wth)
    for z in temperatureLow1:
        z1 = re.findall('\d{2}',str(z))
        temperatureLow.append(z1[0])
    # print(temperatureLow)
    return(temperatureHigh,temperatureLow,wth)
#爬取未来8~15天的天气
def get_8dweather(header,id):
    #最高温度
    htl = []
    #最低温度
    low = []
    #天气
    wth = []
    url = 'http://www.weather.com.cn/weather15d/%s.shtml'%id
    req = requests.get(url,headers = header)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html,'lxml')
    wth1 = bs.select('span[class="wea"]')
    for z in wth1:
        wth.append(z.string)
    htl1 = bs.select('span[class="tem"] em')
    for h in htl1:
        h1 = re.findall('\d{2}',str(h))
        htl.append(h1[0])
    #8-15天的最低温度
    ltl = bs.select('span[class="tem"]')
    for x in ltl:
        l = re.findall('\d{2}',str(x))
        low.append(l[1])
    return(htl,low,wth)
#主函数
def main(n,m):

    header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    # n = input('请输入城市名:')
    # m = input('请输入日期:')
    p = get_id(n)
    p1 = get_7dweather(header,p)
    p2 = get_8dweather(header,p)
    sumht = p1[0] + p2[0]
    sumlt = p1[1] + p2[1]
    sumwea = p1[2] + p2[2]
    return str(show_weather(m,sumht,sumlt,sumwea))

#
# if __name__ == '__main__':
#     n = input('请输入城市名:')
#     m = input('请输入日期:')
#     main(n,m)
