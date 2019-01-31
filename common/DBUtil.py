# -*- coding:utf-8 -*-
from common import IPUtils
from config.ApiKeys import dbname, dbpass, dbaddr

__author__ = 'zhennehz'

# 这个就是为了连接oracle导入的库，个人认为应该就是一个驱动吧！
import cx_Oracle
# 解决乱码
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
'''
    第一个：参数是你的的登录oracle时的用户名
    第二个：参数就是登录密码
    第三个：127.0.0.1:1521就是oracle的ip地址加端口
    第四个：是你的监听服务器的名称，你可以去oracle下的Net Configuration Assistance这儿去修改，有一个地址讲的特别详细
            最后我会贴地址。                                               
'''
'''conn = cx_Oracle.connect(dbname, dbpass, dbaddr)  # 第一个参数是你的的登录oracle时的用户名
cursor = conn.cursor()
cursor.execute('select * from CFG_CITY')
result = cursor.fetchall()
print (cursor.rowcount)
for row in result:
    print(row)'''

# 封装的类
class cxOracle:

    def __init__(self, uname, upwd, tns):
        self._uname = uname
        self._upwd = upwd
        self._tns = tns
        self._conn = None
        self._ReConnect()


    def _ReConnect(self):
        if not self._conn:
            self._conn = cx_Oracle.connect(self._uname, self._upwd, self._tns)
        else:
            pass


    def __del__(self):
        if self._conn:
            self._conn.close()
            self._conn = None


    def _NewCursor(self):
        cur = self._conn.cursor()
        if cur:
            return cur
        else:
            print
            "#Error# Get New Cursor Failed."
            return None


    def _DelCursor(self, cur):
        if cur:
            cur.close()


    # 检查是否允许执行的sql语句
    def _PermitedUpdateSql(self, sql):
        rt = True
        lrsql = sql.lower()
        sql_elems = [lrsql.strip().split()]
        # update和delete最少有四个单词项
        if len(sql_elems) < 4:
            rt = False
        # 更新删除语句，判断首单词，不带where语句的sql不予执行
        elif sql_elems[0] in ['update', 'delete']:
            if 'where' not in sql_elems:
                rt = False

        return rt


    # 导出结果为文件
    def Export(self, sql, file_name, colfg='||'):
        rt = self.Query(sql)
        if rt:
            with open(file_name, 'a') as fd:
                for row in rt:
                    ln_info = ''
                    for col in row:
                        ln_info += str(col) + colfg
                    ln_info += '\n'
                    fd.write(ln_info)


    # 查询
    def Query(self, sql, nStart=0, nNum=- 1):
        rt = []

        # 获取cursor
        cur = self._NewCursor()
        if not cur:
            return rt

        # 查询到列表
        cur.execute(sql)
        if (nStart == 0) and (nNum == 1):
            rt.append(cur.fetchone())
        else:
            rs = cur.fetchall()
            if nNum == - 1:
                rt.extend(rs[nStart:])
            else:
                rt.extend(rs[nStart:nStart + nNum])

        # 释放cursor
        self._DelCursor(cur)

        return rt


    # 更新
    def Exec(self, sql):
        # 获取cursor
        rt = None
        cur = self._NewCursor()
        if not cur:
            return rt

        # 判断sql是否允许其执行
        #if not self._PermitedUpdateSql(sql):
        #    return rt

        # 执行语句
        rt = cur.execute(sql)

        # 提交事务
        self._conn.commit()

        # 释放cursor
        self._DelCursor(cur)

        return rt


# 类使用示例

#tns = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.16.17.46)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=MYDB)))'
'''
ora = cxOracle(dbname, dbpass, dbaddr)

# 导出结果为文件
rs = ora.Export("SELECT * FROM py_poi_point", '1.txt')

# 查询结果到列表
rs = ora.Query("SELECT * FROM py_poi_point")
print(rs)

# 更新数据
ora.Exec("insert into py_poi_point values('C730','2',123,28) ")
'''
'''
path = 'Polygon.txt'  # 存放爬取ip的文档path
IPUtils.truncatefile(path)  # 爬取前清空文档
ora = cxOracle(dbname, dbpass, dbaddr)

# 查询结果到列表
rs = ora.Query("SELECT * FROM py_poi_point where id in(SELECT id FROM PY_POI t where city='C731' AND TYPE LIKE '商务住宅%') order by id,rn")
i = 0
name = ""
print("Polygon")
IPUtils.write(path=path, text="Polygon")
for r in rs:
    if(name!=r[3]):
        print("end")
        IPUtils.write(path=path, text="end")
        i=0
        name = r[3]
        print("Polygon")
        IPUtils.write(path=path, text="Polygon")
    print(str(i)+" "+str(r[4])+" "+str(r[5])+" 1.#QNAN 1.#QNAN")
    IPUtils.write(path=path, text=str(i)+" "+str(r[4])+" "+str(r[5])+" 1.#QNAN 1.#QNAN")
    i=i+1
print("end")
IPUtils.write(path=path, text="end")
'''