# -*- coding:utf-8 -*-
import urllib
from urllib import request

from common.IPUtils import get_IP_list

__author__ = 'zhennehz'

if __name__ == "__main__":
    #get_IP_list()
    '''
    # 访问网址
    url = 'https://ip.cn/'
    # 这是代理IP
    # 这是代理IP
    proxy = {'https': '113.239.226.245:80'}
    # 创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    # 创建Opener
    opener = request.build_opener(proxy_support)
    # 添加User Angent
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    # 安装OPener
    # request.install_opener(opener)
    # 使用自己安装好的Opener
    # response = request.urlopen(url)
    # 如果不想安装也可以直接使用opener来执行
    response = opener.open(url)
    # 读取相应信息并解码
    html = response.read().decode("utf-8")
    # 打印信息
    html = BeautifulSoup(html, 'html.parser')
    print(html.select("#result"))
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Cookie': 'gr_user_id=1f9ea7ea-462a-4a6f-9d55-156631fc6d45; bid=vPYpmmD30-k; ll="118282"; ue="codin; __utmz=30149280.1499577720.27.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/doulist/240962/; __utmv=30149280.3049; _vwo_uuid_v2=F04099A9dd; viewed="27607246_26356432"; ap=1; ps=y; push_noty_num=0; push_doumail_num=0; dbcl2="30496987:gZxPfTZW4y0"; ck=13ey; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1515153574%2C%22https%3A%2F%2Fbook.douban.com%2Fmine%22%5D; __utma=30149280.833870293.1473539740.1514800523.1515153574.50; __utmc=30149280; _pk_id.100001.8cb4=255d8377ad92c57e.1473520329.20.1515153606.1514628010.'
    }

    url = "https://ip.cn/"

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    # 设置代理 IP，http 不行，使用 https
    proxy = request.ProxyHandler({'https': '114.7.15.146:8080'})
    auth = request.HTTPBasicAuthHandler()
    # 构造 opener
    opener = request.build_opener(proxy, auth, request.HTTPHandler)
    # 添加 header
    opener.addheaders = [('User-Agent', user_agent)]
    # 安装 opener
    request.install_opener(opener)
    # 打开链接
    req = urllib.request.Request(url, None, headers)

    conn = request.urlopen(req)
    # 以 utf-8 编码获取网页内容
    content = conn.read().decode('utf-8')
    # 输出
    print(content)
