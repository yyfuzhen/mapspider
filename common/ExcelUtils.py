# -*- coding:utf-8 -*-
__author__ = 'zhennehz'

import json
from urllib import request
from config.ApiKeys import poi_boundary_url

import xlwt as xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# 数据写入excel-POI
def write_to_excel(poilist, classfield, path):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'pname')
    sheet.write(0, 4, 'pcode')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'citycode')
    sheet.write(0, 7, 'adname')
    sheet.write(0, 8, 'adcode')
    sheet.write(0, 9, 'address')
    sheet.write(0, 10, 'type')
    for i in range(len(poilist)):
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['pname'])
        sheet.write(i + 1, 4, poilist[i]['pcode'])
        sheet.write(i + 1, 5, poilist[i]['cityname'])
        sheet.write(i + 1, 6, poilist[i]['citycode'])
        sheet.write(i + 1, 7, poilist[i]['adname'])
        sheet.write(i + 1, 8, poilist[i]['adcode'])
        sheet.write(i + 1, 9, poilist[i]['address'])
        sheet.write(i + 1, 10, poilist[i]['type'])
    book.save(path)
    print('写入成功')

# 追加数据到excel中
def contact_read_excel(poilist, path):
    rexcel = open_workbook(path)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    # print('原有的行', rows)
    for i in range(len(poilist)):
        table.write(rows + i, 0, poilist[i]['id'])
        table.write(rows + i, 1, poilist[i]['name'])
        table.write(rows + i, 2, poilist[i]['location'])
        table.write(rows + i, 3, poilist[i]['pname'])
        table.write(rows + i, 4, poilist[i]['pcode'])
        table.write(rows + i, 5, poilist[i]['cityname'])
        table.write(rows + i, 6, poilist[i]['citycode'])
        table.write(rows + i, 7, poilist[i]['adname'])
        table.write(rows + i, 8, poilist[i]['adcode'])
        table.write(rows + i, 9, poilist[i]['address'])
        table.write(rows + i, 10, poilist[i]['type'])

    excel.save(path)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
    print('追加成功')


# 数据读取excel-POI
def read_to_excel(classfiled,path1,path2):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfiled, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    # 读取excel
    rexcel = open_workbook(path1)  # 用wlrd提供的方法读取一个excel文件
    sheet2 = rexcel.sheets()[0]
    nrows = sheet2.nrows  # 用wlrd提供的方法获得现在已有的行数
    # 获取整行和整列的值（数组）
    for i in range(nrows):
        if(i==0):
            continue
        rows = sheet2.row_values(i)  # 获取第四行内容
        id = rows[0]
        name = rows[1]
        # 根据poi的id获取边界数据
        bounstr = ''
        print(id)
        bounlist = getBounByIdNew(id)
        if (len(bounlist) > 1):
            bounstr = str(bounlist)
        # 每一行写入
        sheet.write(i, 0, id)
        sheet.write(i, 1, name)
        sheet.write(i, 2, bounstr)
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(path2)
    print('追加成功')


# 根据id获取边界数据
def getBounByIdNew(id):
    req_url = poi_boundary_url + "?id=" + id
    with request.urlopen(req_url) as f:
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
