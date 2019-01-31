# -*- coding:utf-8 -*-
import requests

from config.ApiKeys import PROXY_POOL_URL

__author__ = 'zhennehz'



def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None



if __name__ == "__main__":
    print(get_proxy())