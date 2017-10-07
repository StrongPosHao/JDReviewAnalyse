# -*- coding: utf-8 -*-

import requests
import bs4
from bs4 import BeautifulSoup
import re


def getHTML(url):
    r = requests.get(url, headers = {'user-agent': 'Mozilla/5.0'})
    r.encoding = r.apparent_encoding
    if r.status_code != 200:
        raise Exception('NetworkError!')
    return r.text.encode('utf-8')

def getURL(productID, pageNum):
    url1 = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv14911&productId='
    url2 = 'page='
    url3 = '&pageSize=10&isShadowSku=0&fold=1'
    url2 += str(pageNum)
    return url1 + str(productID) + '&score=0&sortType=5&' + url2 + url3

def getHTMLByPages(pageNum):
    res = []
    for i in range(pageNum):
        res.append(getHTML(getURL(i)))
    return res

def getComments(htmls):
    res = []
    for html in htmls:
        content = re.findall(r'"guid".*?,"content":(.*?),', html)
        for i in content:
            comment = re.split(r"(<div class='uploadimgdiv'>)", i, maxsplit = 1)
            comment = comment[0].replace(r"\n", " ").strip()
            res.append(comment)
    return res

def getHardwareInfo(html):
    soup = BeautifulSoup(html, 'html.parser')
    Item = soup.find('div', class_ = "Ptable")
    return Item.get_text()
    
def getProductName(html):
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('div', class_ = 'sku-name').string.strip()
    return name
    
def saveFileComments(path, list1):
    with open(path, 'a') as f:
        for i in list1:
            f.write(i)
            f.write("\n----------------------------------------------------------------------------------------------------------\n")

def saveFileName(path, name):
    with open(path, 'a') as f:
        f.write(name.encode('utf-8'))
        
def saveFileInfo(path, info):
    with open(path, 'a') as f:
        f.write(info.encode('utf-8'))

if __name__ == '__main__':
    saveFileComments('comments.txt', getComments(getHTMLByPages(2)))
    saveFileName('info.txt', getProductName(getHTML('https://item.jd.com/5025518.html#product-detail')))
    saveFileInfo('info.txt', getHardwareInfo(getHTML('https://item.jd.com/5025518.html#product-detail')))
    print 'OK!'
   
    
