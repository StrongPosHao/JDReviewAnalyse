#encoding: utf-8

import requests
from bs4 import BeautifulSoup
import re

class BasicCrawler(object):

    def getHTML(self, url):
        r = requests.get(url, headers = {'user-agent': 'Mozilla/5.0'})
        r.encoding = r.apparent_encoding
        if r.status_code != 200:
            print r.status_code
            raise Exception('NetworkError!')
        return r.text

    def getURL(self, pageNum, productID):
        url1 = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv14911&productId='
        url2 = 'page='
        url3 = '&pageSize=10&isShadowSku=0&fold=1'
        url2 += str(pageNum)
        return url1 + str(productID) + '&score=0&sortType=5&' + url2 + url3

    def recordError(self, productID, errorType):
        with open(r'../Data/errorID.txt', 'a') as f2:
            f2.write(str(productID) + '    ' + errorType + '\n')


