# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import json
import sys
import codecs

def getHTML(url):
    r'''
    Get the HTML text by the provided url.
    :param url:
    :return: HTML text
    '''
    r = requests.get(url, headers = {'user-agent': 'Mozilla/5.0'})
    r.encoding = r.apparent_encoding
    if r.status_code != 200:
        print r.status_code
        raise Exception('NetworkError!')
    return r.text

def getURL(productID, pageNum):
    r'''
    Get the URL by productID and page number.
    :param productID:
    :param pageNum:
    :return: URL
    '''
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

def getComments(html):
    # res = []
    # # for html in htmls:
    # content = re.findall(r'"guid".*?,"content":(.*?),', html)
    # for i in content:
    #     comment = re.split(r"(<div class='uploadimgdiv'>)", i, maxsplit = 1)
    #     comment = comment[0].replace(r"\n", " ").strip().decode('utf-8')
    #     res.append(comment)
    # return res
    res = []
    s = html[27 : -2]
    try:
        j = json.loads(s)
    except ValueError, e:
        print "ValueError"
        return res
    for i in j['comments']:
            res.append(i['content'])
    return res

def getHardwareInfo(html):
    soup = BeautifulSoup(html, 'html.parser')
    Item = soup.find('div', class_ = "Ptable")
    with open() as f:
        for i in Item.find_all('dl'):
            f.write(i.dl.string + ':' + i.dd.string)
    return Item.get_text().strip().encode('utf-8')
    
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

def getBasicInfo(data, breakpoint):
    productName = data['Name']
    productID = data['ID']
    breakpoint_record = data['breakpoint']
    with open(r'../Data/breakpoint.txt', 'r') as f:
        breakpoint = f.readline()
    breakpoint = int(breakpoint)
    while True:
        for i in range(breakpoint, breakpoint + 1):
            folder_path = r'../Data/' + productID[i]
            try:
                os.mkdir(folder_path)
            except WindowsError, e:
                print str(productID[i]) + 'already exists' + '\n'
            html = getHTML('https://item.jd.com/' + productID[i] + '.html#product-detail')
            soup = BeautifulSoup(html, 'html.parser')
            Item = soup.find('div', class_="Ptable")
            with open(folder_path + '/basicInfo.txt', 'w') as f:
                f.write(productName[i] + '\n' * 2)
                try:
                    print 'OK' + productID[i]
                    for j in Item.find_all('div', class_ = "Ptable-item"):
                        f.write(j.h3.string.encode('utf-8').strip() + "\n\n")
                        for k, h in zip(j.dl.find_all('dt'), j.dl.find_all('dd')):
                            f.write(k.string.encode('utf-8') + ": " + h.string.encode('utf-8') + '\n')
                        f.write('\n'*4)
                except Exception, e:
                    print productID[i] + '      getHardwareInfoError'
                    with open(r'../Data/errorID.txt', 'a') as f:
                        f.write(str(productID[i]) + '\n')
            with open(r'../Data/breakpoint.txt', 'w') as f:
                f.write(str(i))
        breakpoint += 10

if __name__ == '__main__':
    with open(r'../Data/breakpoint.txt', 'r') as f:
        breakpoint = f.readline()
    breakpoint = int(breakpoint)
    data = pd.read_csv(r'../ProductURLData/productID.csv')
    productName = data['Name']
    productID = data['ID']
    breakpoint_record = data['breakpoint']
    while True:
        for i in range(breakpoint, breakpoint + 1):
            folder_path = r'../Data/' + productID[i]
            try:
                os.mkdir(folder_path)
            except WindowsError, e:
                print str(productID[i] + 'already exists') + '\n'
                continue
            html = getHTML('https://item.jd.com/' + productID[i] + '.html#product-detail')
            soup = BeautifulSoup(html, 'html.parser')
            Item = soup.find('div', class_="Ptable")
            with open(folder_path + '/basicInfo.txt', 'w') as f:
                f.write(productName[i] + '\n' * 2)
                try:
                    print 'OK' + productID[i]
                    for j in Item.find_all('div', class_="Ptable-item"):
                        f.write(j.h3.string.encode('utf-8').strip() + "\n\n")
                        for k, h in zip(j.dl.find_all('dt'), j.dl.find_all('dd')):
                            f.write(k.string.encode('utf-8') + ": " + h.string.encode('utf-8') + '\n')
                        f.write('\n' * 4)
                except Exception, e:
                    print productID[i] + '      getBasicInfoError'
                    with open(r'../Data/errorID.txt', 'a') as f2:
                        f2.write(str(productID[i]) + '  get_basicinfo error!' + '\n')
                for page in range(0, 300):
                    try:
                        url = getURL(productID[i], page)
                        review_html = getHTML(url)
                    except Exception, e:
                        print i
                        print productID[i].encode('utf-8') + ' ' + str(page) + 'get_html error!'
                        with open(r'../Data/errorID.txt', 'a') as f2:
                            f2.write(str(productID[i]) + '  get_html error!' + '\n')
                    with codecs.open(folder_path + "/reviews.txt", 'a', encoding='utf-8') as f1:
                        comments = getComments(review_html)
                        if len(comments) == 0:
                            print 'value error!'
                            with open(r'../Data/errorID.txt', 'a') as f2:
                                f2.write(str(productID[i]) + 'value error!' + '\n')
                                continue
                        for comment in comments:
                            try:
                                f1.write(comment)
                                f1.write('\r\n')
                                f1.write('-------------------------------------------------------------------------------------------------------------------------------------------------------------' + '\r\n')
                            except Exception,e:
                                print 'Unicode Error'
            with open(r'../Data/breakpoint.txt', 'w') as f3:
                f3.write(str(i))
        breakpoint += 1



    
