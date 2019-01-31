# -*- coding:utf-8 -*-
import random

__author__ = 'zhennehz'

import time

from common.DBUtil import cxOracle
from common.GeoUtils import wgs84togcj02, gcj02towgs84, ComputeArea
from common.POIUtils import getpois, getbouns, getpolygonpois, getBounById, getBounById2, get_proxy
from config.ApiKeys import local_root, dbname, dbpass, dbaddr, city_list, poi_type_list, city_id_list

cityIndex = input("请输入城市编号:\n['0-岳阳', '1-长沙', '2-湘潭', '3-株洲', '4-衡阳', '5-郴州', '6-常德', "
             "\n '7-益阳', '8-娄底', '9-邵阳', '10-湘西', '11-张家界', '12-怀化', '13-永州']\n")
typeIndex = input("请输入爬取场景类型编号(回车查询全部):\n['0-汽车服务', '1-汽车销售', '2-汽车维修', '3-摩托车服务', '4-餐饮服务', '5-购物服务', \n "
             "'6-生活服务', '7-体育休闲服务', '8-医疗保健服务', '9-住宿服务', '10-风景名胜', '11-商务住宅', '12-政府机构及社会团体', \n "
             "'13-科教文化服务', '14-交通设施服务', '15-金融保险服务', '16-公司企业', '17-道路附属设施', '18-公共设施', '19-地名地址信息']\n")

city = city_list[int(cityIndex)]
city_id = city_id_list[int(cityIndex)]
sqlparam = ""
if typeIndex!='':
    poi_type = poi_type_list[int(typeIndex)]
    sqlparam = " and ptype = '"+poi_type+"'"
else:
    poi_type = "全部"
print("查询"+city+"的"+poi_type+"数据")
#查询对应city的grid1600数据
ora = cxOracle(dbname, dbpass, dbaddr)


# 先删除异常表中爬取的ID的数据
print("删除异常表中的ID爬取的数据")
#ora.Exec("DELETE PY_POI_POINT WHERE CITY='"+city_id+"' "+sqlparam+" AND ID IN(SELECT ID FROM PY_POI_EXCEPTION WHERE CITY ='"+city_id+"' "+sqlparam+") ")
#ora.Exec("DELETE PY_POI_EXCEPTION WHERE CITY ='"+city_id+"' "+sqlparam+" ")

# 查询栅格表
rs = ora.Query("SELECT city, gridid, ptype, id, name FROM PY_POI WHERE CITY ='"+city_id+"' "+sqlparam+" "
            "AND ID NOT IN (SELECT ID FROM PY_POI_POINT WHERE CITY ='"+city_id+"' "+sqlparam+") AND ISSEL IS NULL "
            "ORDER BY GRIDID ASC ")

proxy_ip = get_proxy()
if proxy_ip == None:
   raise NameError('代理池返回ip为空')

for f in rs:
    print("GRID="+str(f[1])+",ID="+str(f[3]))
    OBJECTID = str(f[1])
    id = str(f[3])
    id = "B0FFGFHRBZ"
    while True:  # 使用while循环不断获取数据
        datas = ""
        area = 0
        try:
            bouns = getBounById2(id,proxy_ip)
            for bound in bouns:
                if bound != None:
                    lon = bound[0]
                    lat = bound[1]
                    area = bound[2]
                    datas += str(lon) + "," + str(lat) + ";"
            if abs(area - ComputeArea(datas[:-1])) < 1:
                for bound in bouns:
                    if bound != None:
                        lon = bound[0]
                        lat = bound[1]
                        lon, lat = gcj02towgs84(float(lon), float(lat))
                        sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi_type+"','" + id + "'," + str(
                            lon) + "," + str(lat) + ")"
                        ora.Exec(sql2)
                break
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
    sql4 = "UPDATE PY_POI SET ISSEL = '1' WHERE ID = '" + id + "' "
    ora.Exec(sql4)
print("爬取完成")