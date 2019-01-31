# -*- coding:utf-8 -*-
import math
import random
import threading

__author__ = 'zhennehz'

import time

from common.DBUtil import cxOracle
from common.GeoUtils import wgs84togcj02, gcj02towgs84, ComputeArea
from common.POIUtils import getpois, getbouns, getpolygonpois, getBounById, getBounById2, get_proxy, getBounById3
from config.ApiKeys import local_root, dbname, dbpass, dbaddr, city_list, poi_type_list, city_id_list


city = '长沙'
city_id = 'C731'
#风景名胜
poi_type = '商务住宅'

def spider(startIndex,endIndex):
    sqlparam = " and ptype = '"+poi_type+"'"
    sqlstart = " and tt.rowno >="+startIndex
    sqlend = " and rownum <="+endIndex

    print("查询"+city+"的"+poi_type+"数据")

    #查询对应city的grid1600数据
    ora = cxOracle(dbname, dbpass, dbaddr)

    # 查询栅格表
    rs = ora.Query("select tt.* from ("
                "select t.*,rownum as rowno from("
                "SELECT city, gridid, ptype, id, name FROM PY_POI WHERE CITY ='"+city_id+"' "+sqlparam+" "
                "AND ID NOT IN (SELECT ID FROM PY_POI_POINT WHERE CITY ='"+city_id+"' "+sqlparam+") AND (ISSEL IS NULL or ISBONS ='1')"
                "ORDER BY GRIDID ASC)t where 1=1 "+sqlend+")tt where 1=1 "+sqlstart)

    proxy_ip = get_proxy()
    if proxy_ip == None:
        raise NameError('代理池返回ip为空')

    for f in rs:
        print("GRID="+str(f[1])+",ID="+str(f[3]))
        OBJECTID = str(f[1])
        id = str(f[3])
        while True:  # 使用while循环不断获取数据
            datas = ""
            area = 0
            try:
                bouns = getBounById2(id,proxy_ip)
                #bouns = getBounById(id)
                print("bouns="+str(bouns))
                for bound in bouns:
                    if bound != None:
                        lon = bound[0]
                        lat = bound[1]
                        area = bound[2]
                        datas += str(lon) + "," + str(lat) + ";"
                print("area="+str(area)+",datas="+str(datas))
                print("ComputeArea=" + str(ComputeArea(datas[:-1])) )
                if abs(area - ComputeArea(datas[:-1])) < 2000:
                    for bound in bouns:
                        if bound != None:
                            lon = bound[0]
                            lat = bound[1]
                            lon1, lat1 = gcj02towgs84(float(lon), float(lat))
                            sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi_type+"','" + id + "'," + str(
                                lon) + "," + str(lat) + "," + str(
                                lon1) + "," + str(lat1) + ")"
                            ora.Exec(sql2)
                    break
                time.sleep(random.randint(1, 3))
            except Exception as e:
                e = str(e).replace('\'', '`')
                print(e)
                sql3 = "insert into PY_POI_EXCEPTION values('" + city_id + "','" + OBJECTID + "','" + poi_type + "','" + id + "','" + e + "',sysdate)"
                ora.Exec(sql3)
                # 换ip
                proxy_ip = get_proxy()
                if proxy_ip == None:
                    raise NameError('代理池返回ip为空')
        # 更新poi字段为已查询
        sql4 = ""
        if area == 0:
            sql4 = "UPDATE PY_POI SET ISSEL = '1',ISBONS = '0' WHERE ID = '" + id + "' "
        else:
            sql4 = "UPDATE PY_POI SET ISSEL = '1',ISBONS = '1' WHERE ID = '" + id + "' "
        ora.Exec(sql4)
        time.sleep(random.randint(1, 3))
    print(city+":"+poi_type+"的"+startIndex+"-"+endIndex+"的数据爬取完成")


#设置总记录数和线程数
tot = 9083
count = 1
step = math.ceil(tot/count)
arr1 = []
arr2 = []
for i in range(count):
    # print("index:"+str(i+1)+ " from:"+str(i*step+1)+" to:"+str((i+1)*step))
    arr1.append(str(i*step+1))
    arr2.append(str((i+1)*step))


#创建线程
threads = []
files = range(len(arr1))

for i in range(len(arr1)):
    # print(str(arr1[i])+"--"+str(arr2[i]))
    t = threading.Thread(target=spider, args=(arr1[i], arr2[i]))
    threads.append(t)

if __name__ == '__main__':

    # 启动线程
    for k in files:
        threads[k].start()
    for k in files:
        threads[k].join()

    print("所有进程执行完毕 %s" % time.ctime())