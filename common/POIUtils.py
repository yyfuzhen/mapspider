# -*- coding:utf-8 -*-
import random
import urllib

import requests

__author__ = 'zhennehz'

from common.ExcelUtils import write_to_excel, contact_read_excel, read_to_excel
from config.ApiKeys import amap_web_key, poi_search_url, poi_boundary_url, poi_polygon_url, map_key_list, \
    PROXY_POOL_URL, agents, proxyHost, proxyPort, proxyUser, proxyPass
from urllib.parse import quote
from urllib import request
import json

# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords ,path):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['status'] is not '1':
            return
        if len(result['pois']) < 25:
            hand(poilist, result)
            write_to_excel(poilist, keywords, path)
            break
        hand(poilist, result)
        if i == 1:
            write_to_excel(poilist, keywords, path)
        else:
            contact_read_excel(poilist, path)
        i = i + 1
    return poilist


# 根据城市名称和分类和经纬度关键字获取poi数据
def getpolygonpois(cityname,keywords,lon1, lat1, lon2, lat2):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        polygon = str(lon1)+','+str(lat1)+'|'+str(lon2)+','+str(lat2)
        result = getpoi_page3(cityname, keywords, i,polygon)
        result = json.loads(result)  # 将字符串转换为json
        if result['status'] is not '1':
            return
        if len(result['pois']) < 25:
            hand(poilist, result)
            break
        hand(poilist, result)
        i = i + 1
    return poilist



# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url,timeout=1) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

# 单页范围获取pois
def getpoi_page2(cityname, keywords, page,polygon):
    req_url = poi_polygon_url + "?key=" + map_key_list[random.randint(0,29)] + '&extensions=all&polygon=' +polygon + '&types=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    print(req_url)
    data = ''
    with request.urlopen(req_url,timeout=1) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

# 根据代理ip请求单页范围获取pois
def getpoi_page3(cityname, keywords, page,polygon):
    proxy_ip = get_proxy()
    if proxy_ip == None:
        raise NameError('代理池返回ip为空')

    req_url = poi_polygon_url + "?key=" + map_key_list[random.randint(0,29)] + '&extensions=all&polygon=' +polygon + '&types=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    print(req_url)
    # 随机取头部信息
    user_agent = agents[random.randint(0, len(agents) - 1)]
    # 设置代理 IP，http 不行，使用 https
    proxy = request.ProxyHandler({'https': proxy_ip})
    auth = request.HTTPBasicAuthHandler()
    # 构造 opener
    opener = request.build_opener(proxy, auth, request.HTTPHandler)
    # 添加 header
    opener.addheaders = [('User-Agent', user_agent)]
    # 安装 opener
    request.install_opener(opener)
    data = ''
    # 打开链接
    with request.urlopen(req_url,timeout=10) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

# 根据城市名称和分类关键字获取边界点数据
def getbouns(classfiled,path1,path2):
    bounlist = []
    read_to_excel(classfiled,path1,path2)
    return bounlist


# 根据id获取边界数据
def getBounById(id):
    req_url = poi_boundary_url + "?id=" + id
    print(req_url)
    with request.urlopen(req_url,timeout=1) as f:
        data = f.read()
        data = data.decode('utf-8')
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                innerList = []
                f1 = float(i.split(',')[0])
                innerList.append(float(i.split(',')[0]))
                innerList.append(float(i.split(',')[1]))
                dataList.append(innerList)
        return dataList

# 使用代理ip根据id获取边界数据
def getBounById2(id,proxy_ip):
    #proxy_ip = get_proxy()
    #if proxy_ip == None:
    #   raise NameError('代理池返回ip为空')

    req_url = poi_boundary_url + "?id=" + id
    print(req_url)

    # 随机取头部信息
    user_agent = agents[random.randint(0, len(agents) - 1)]
    # 设置代理 IP，http 不行，使用 https
    proxy = request.ProxyHandler({'https': proxy_ip})
    auth = request.HTTPBasicAuthHandler()
    # 构造 opener
    opener = request.build_opener(proxy, auth, request.HTTPHandler)
    # 添加 header
    headers = {
        'Cookie': "guid=93fe-1614-3b4b-9ae6; UM_distinctid=166c2fa3a9769-06c3a9533caf26-43450521-13c680-166c2fa3a982a; cna=rUsPEl1BQTECAa8KBECvqZYC; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=2067366097-1540864364-%7C1540973390; x5sec=7b22617365727665723b32223a223064323038383531343766373036646537633131613839343637656133666538434f335435643446454f724e356f75506a3837783567453d227d; isg=BNzcbtpb6zbYxp9kq5KAnRj1rfpO_YEkjAK3Frbd60eqAXyL3mRVDla3ZSlcibjX",
        'Referer': "https://www.amap.com/place/" + id,
        'User-Agent': user_agent
    }
    # 添加 header
    #opener.addheaders = [('User-Agent', user_agent)]
    req = urllib.request.Request(req_url, None, headers)
    # 安装 opener
    request.install_opener(opener)
    # 打开链接
    with request.urlopen(req,timeout=10) as f:
        data = f.read()
        data = data.decode('utf-8')
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        if(datajson['status']=='8'):
            return dataList
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            area = datajson['area']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                # 有的经纬度返回有|特殊处理
                if i.find('|')>=0:
                    innerList = []
                    f1 = float(i.split('|')[0].split(',')[0])
                    innerList.append(float(i.split('|')[0].split(',')[0]))
                    innerList.append(float(i.split('|')[0].split(',')[1]))
                    innerList.append(float(area))
                    dataList.append(innerList)
                else:
                    innerList = []
                    f1 = float(i.split(',')[0])
                    innerList.append(float(i.split(',')[0]))
                    innerList.append(float(i.split(',')[1]))
                    innerList.append(float(area))
                    dataList.append(innerList)
        return dataList

# 使用阿布云代理ip获取边界数据
def getBounById3(id):
    req_url = poi_boundary_url + "?id=" + id
    print(req_url)

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxy_handler = request.ProxyHandler({
        "http": proxyMeta,
        "https": proxyMeta,
    })
    auth = request.HTTPBasicAuthHandler()
    # opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

    # 添加 header
    user_agent = agents[random.randint(0, len(agents) - 1)]
    headers = {
        'Cookie': "guid=93fe-1614-3b4b-9ae6; UM_distinctid=166c2fa3a9769-06c3a9533caf26-43450521-13c680-166c2fa3a982a; cna=rUsPEl1BQTECAa8KBECvqZYC; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=2067366097-1540864364-%7C1541037202; x5sec=7b22617365727665723b32223a223839623439316565306638313962386663376234393634353461376239363137434b626336643446454d4c626d706e76386676697067453d227d; isg=BFBQCmP3PwlohOMAN07UMWxxIZ5isTU42AarMkohHKt-hfAv8ikE86azWQ3AVew7",
        'Referer': "https://www.amap.com/place/" + id,
        'User-Agent': user_agent
    }
    opener = request.build_opener(proxy_handler)
    #opener.addheaders = [("Proxy-Switch-Ip", "yes")]
    request.install_opener(opener)
    req = urllib.request.Request(req_url, None, headers)
    # 打开链接
    with request.urlopen(req,timeout=10) as f:
        data = f.read()
        data = data.decode('utf-8')
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        if(datajson['status']=='8'):
            return dataList
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            area = datajson['area']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                # 有的经纬度返回有|特殊处理
                if i.find('|')>=0:
                    innerList = []
                    f1 = float(i.split('|')[0].split(',')[0])
                    innerList.append(float(i.split('|')[0].split(',')[0]))
                    innerList.append(float(i.split('|')[0].split(',')[1]))
                    innerList.append(float(area))
                    dataList.append(innerList)
                else:
                    innerList = []
                    f1 = float(i.split(',')[0])
                    innerList.append(float(i.split(',')[0]))
                    innerList.append(float(i.split(',')[1]))
                    innerList.append(float(area))
                    dataList.append(innerList)
        return dataList


# 代理池获取代理ip
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None