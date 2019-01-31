# -*- coding:utf-8 -*-
__author__ = 'zhennehz'

import time

from common.DBUtil import cxOracle
from common.GeoUtils import wgs84togcj02, gcj02towgs84
from common.POIUtils import getpois, getbouns, getpolygonpois, getBounById, getBounById2
from config.ApiKeys import local_root, dbname, dbpass, dbaddr, city_list, poi_type_list, city_id_list

# 获取城市分类数据
#cityname = "岳阳"
#classfiled = "大学"
#path = local_root+cityname+classfiled+".xls";
#pathbouns = local_root+cityname+classfiled+"边界.xls";

#pois = getpois(cityname, classfiled, path)
#bouns = getbouns(classfiled,path,pathbouns)

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

# 先删除异常表中爬取的gridid的数据
print("删除异常表中的GRIDID爬取的数据")
ora.Exec("DELETE PY_POI_POINT WHERE CITY='"+city_id+"' "+sqlparam+" AND GRIDID IN(SELECT GRIDID FROM PY_POI_EXCEPTION WHERE CITY ='"+city_id+"' "+sqlparam+") ")
ora.Exec("DELETE PY_POI WHERE CITY='"+city_id+"' "+sqlparam+" AND GRIDID IN(SELECT GRIDID FROM PY_POI_EXCEPTION WHERE CITY ='"+city_id+"' "+sqlparam+")  ")
ora.Exec("DELETE PY_POI_EXCEPTION WHERE CITY ='"+city_id+"' "+sqlparam+" ")

# 查询栅格表
# rs = ora.Query("SELECT OBJECTID,MIN_X,MIN_Y,MAX_X,MAX_Y FROM CFG_"+city_id+"_FISHNET1600")
rs = ora.Query("SELECT GRIDID OBJECTID,MIN_X,MIN_Y,MAX_X,MAX_Y FROM 长沙3200 a "
               "WHERE GRIDID NOT IN(SELECT GRIDID FROM PY_POI WHERE CITY ='"+city_id+"' "+sqlparam+" GROUP BY GRIDID) "
               "order by Gridid asc")
for f in rs:
    OBJECTID = str(f[0])
    MIN_X = f[1]
    MIN_Y = f[2]
    MAX_X = f[3]
    MAX_Y = f[4]
    # 转成高德火星坐标
    gcjxy1 = wgs84togcj02(MIN_X,MIN_Y)
    gcjx1 = gcjxy1[0]
    gcjy1 = gcjxy1[1]
    gcjxy2 = wgs84togcj02(MAX_X,MAX_Y)
    gcjx2 = gcjxy2[0]
    gcjy2 = gcjxy2[1]
    print("OBJECTID="+OBJECTID)
    id = ""
    if poi_type!="全部":
        try:
            pois = getpolygonpois(city, poi_type, gcjx1,gcjy1,gcjx2,gcjy2)
            print(pois)
            for i in range(len(pois)):
                if pois != None:
                    id = pois[i]['id']
                    name = pois[i]['name']
                    center_x,center_y = pois[i]['location'].split(",")
                    pname = pois[i]['pname']
                    pcode = pois[i]['pcode']
                    cityname = pois[i]['cityname']
                    citycode = pois[i]['citycode']
                    adname = pois[i]['adname']
                    adcode = pois[i]['adcode']
                    address = pois[i]['address']
                    if len(address)==0:
                        address = ""
                    type = pois[i]['type']
                    # 插入数据
                    center_x,center_y = gcj02towgs84(float(center_x),float(center_y))
                    sql = "insert into py_poi values('"+city_id+"','"+OBJECTID+"','"+poi_type+"','"+id+"','"+name+"',"+str(center_x)+","+str(center_y)+",'"+pname+"','"+pcode+"','"+cityname+"','"+citycode+"','"+adname+"','"+adcode+"','"+address+"','"+type+"') "
                    ora.Exec(sql)
                    # 查找边界并插入
                    try:
                        bouns = getBounById2(id)
                        for bound in bouns:
                            if bound != None:
                                lon = bound[0]
                                lat = bound[1]
                                lon, lat = gcj02towgs84(float(lon), float(lat))
                                sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi_type+"','" + id + "'," + str(
                                    lon) + "," + str(lat) + ")"
                                ora.Exec(sql2)
                    except:
                        bouns = getBounById2(id)
                        for bound in bouns:
                            if bound != None:
                                lon = bound[0]
                                lat = bound[1]
                                lon, lat = gcj02towgs84(float(lon), float(lat))
                                sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi_type+"','" + id + "'," + str(
                                    lon) + "," + str(lat) + ")"
                                ora.Exec(sql2)
        except Exception as e:
            e = str(e).replace('\'','`')
            print(e)
            sql3 = "insert into PY_POI_EXCEPTION values('"+city_id+"','"+OBJECTID+"','"+poi_type+"','" + id + "','"+e+"',sysdate)"
            ora.Exec(sql3)
        #time.sleep(1)
    else:
        for poi in poi_type_list:
            try:
                pois = getpolygonpois(city, poi, gcjx1, gcjy1, gcjx2, gcjy2)
                print(pois)
                for i in range(len(pois)):
                    if pois != None:
                        id = pois[i]['id']
                        name = pois[i]['name']
                        center_x, center_y = pois[i]['location'].split(",")
                        pname = pois[i]['pname']
                        pcode = pois[i]['pcode']
                        cityname = pois[i]['cityname']
                        citycode = pois[i]['citycode']
                        adname = pois[i]['adname']
                        adcode = pois[i]['adcode']
                        address = pois[i]['address']
                        if len(address) == 0:
                            address = ""
                        type = pois[i]['type']
                        # 插入数据
                        center_x, center_y = gcj02towgs84(float(center_x), float(center_y))
                        sql = "insert into py_poi values('" + city_id + "','"+OBJECTID+"','"+poi+"','" + id + "','" + name + "'," + str(
                            center_x) + "," + str(
                            center_y) + ",'" + pname + "','" + pcode + "','" + cityname + "','" + citycode + "','" + adname + "','" + adcode + "','" + address + "','" + type + "') "
                        ora.Exec(sql)
                        # 查找边界并插入
                        try:
                            bouns = getBounById2(id)
                            for bound in bouns:
                                if bound != None:
                                    lon = bound[0]
                                    lat = bound[1]
                                    lon, lat = gcj02towgs84(float(lon), float(lat))
                                    sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi+"','" + id + "'," + str(
                                        lon) + "," + str(lat) + ")"
                                    ora.Exec(sql2)
                        except:
                            bouns = getBounById2(id)
                            for bound in bouns:
                                if bound != None:
                                    lon = bound[0]
                                    lat = bound[1]
                                    lon, lat = gcj02towgs84(float(lon), float(lat))
                                    sql2 = "insert into py_poi_point values('" + city_id + "','"+OBJECTID+"','"+poi+"','" + id + "'," + str(
                                        lon) + "," + str(lat) + ")"
                                    ora.Exec(sql2)
            except Exception as e:
                e = str(e).replace('\'', '`')
                print(e)
                sql3 = "insert into PY_POI_EXCEPTION values('" + city_id + "','"+OBJECTID+"','"+poi+"','" + id + "','" + e + "',sysdate)"
                ora.Exec(sql3)
            #time.sleep(1)
print("爬取完成")