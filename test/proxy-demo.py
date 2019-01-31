#! -*- encoding:utf-8 -*-
import random
import urllib
from urllib import request
import ssl

from config.ApiKeys import agents

ssl._create_default_https_context = ssl._create_unverified_context
# 要访问的目标页面
#targetUrl = "http://test.abuyun.com/proxy.php"
targetUrl = "https://ditu.amap.com/detail/get/detail?id=B02DB0YRYI"
#targetUrl = "http://proxy.abuyun.com/switch-ip"
#targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H95J0Q2026Y96A7D"
proxyPass = "11DF6B4076503EA4"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxy_handler = request.ProxyHandler({
    "http"  : proxyMeta,
    "https" : proxyMeta,
})

# 添加 header
headers = {
    'Cookie': "guid=93fe-1614-3b4b-9ae6; UM_distinctid=166c2fa3a9769-06c3a9533caf26-43450521-13c680-166c2fa3a982a; cna=rUsPEl1BQTECAa8KBECvqZYC; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=2067366097-1540864364-%7C1540946379; isg=BAgI4gcjx_MD7yt4v_YcWWSJ2XbaGW3gwO5jasK5VAN2nagHasE8S56bETVIrSST",
    'Referer': "https://www.amap.com/place/B02DB0YRYI"
}


auth = request.HTTPBasicAuthHandler()
opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)
#opener = request.build_opener(proxy_handler)
#opener.addheaders = [("Proxy-Switch-Ip", "yes")]

req = urllib.request.Request(targetUrl, None, headers)
request.install_opener(opener)

#for i in range(10):
resp = request.urlopen(req).read()
data = resp.decode('utf-8')

print (data)