# -*- coding:utf-8 -*-
import random

__author__ = 'zhennehz'

import time

from common.DBUtil import cxOracle
from common.GeoUtils import wgs84togcj02, gcj02towgs84, ComputeArea
from common.POIUtils import getpois, getbouns, getpolygonpois, getBounById, getBounById2
from config.ApiKeys import local_root, dbname, dbpass, dbaddr, city_list, poi_type_list, city_id_list

ora = cxOracle(dbname, dbpass, dbaddr)

while True:  # 使用while循环不断获取数据
    id = "B02DB0ZDR8"
    datas = ""
    area = 0
    bouns = getBounById2(id)
    for bound in bouns:
        if bound != None:
            lon = bound[0]
            lat = bound[1]
            area = bound[2]
            datas+=str(lon)+","+str(lat)+";"
    if abs(area-ComputeArea(datas[:-1]))<1:
        for bound in bouns:
            if bound != None:
                lon = bound[0]
                lat = bound[1]
                lon, lat = gcj02towgs84(float(lon), float(lat))
                print(str(lon) + "," + str(lat))
                #sql2 = "insert into py_poi_point values('C731','0','医疗保健服务','" + id + "'," + str(
                #    lon) + "," + str(lat) + ")"
                #ora.Exec(sql2)
        break
    time.sleep(random.randint(5, 15))
print("爬取完成")