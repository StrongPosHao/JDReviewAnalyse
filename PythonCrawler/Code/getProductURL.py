#encoding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import xlrd
import pandas
from pandas import DataFrame


def getHTML(url):
    r'''
    Get the HTML text by the provided url
    :param url:
    :return: HTML text
    '''
    r = requests.get(url, headers = {'user-agent': 'Mozilla/5.0'})
    r.encoding = r.apparent_encoding
    if r.status_code != 200:
        raise Exception('NetworkError')
    return r.text.encode('utf-8')


def getURLByPages(pageNum):
    r'''
    Get product list URL by page number.
    :param pageNum:
    :return product list URL
    '''
    url1 = "https://list.jd.com/list.html?cat=670,671,672&"
    url2 = "page="
    url3 = "&sort=sort_totalsales15_desc&trans=1&JL=6_0_0&ms=6#J_main"
    url2 += str(pageNum)
    return url1 + url2 + url3

def getProductURL(breakpoint):
    r'''
    Get the name and url link of the product
    :param breakpoint:
    :return:
    '''
    for i in range(breakpoint, 1077):
        try:
            html = getHTML(getURLByPages(i))
        except Exception, e:
            print 'ERROR'
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('a', attrs={'title': re.compile(r'^('')'), 'target': "_blank"})
        with open(r'..\ProductURLData\URL.csv', 'a') as f:
            for tag in tags:
                # if tag is None or tag.em.string is None:
                try:
                    f.write(tag.em.text[5:].strip().encode('utf-8') + ',' + str("https:" + tag['href']) + ',' + str(i) + '\n')
                except AttributeError, e:
                    print e.message
            print str(i) + ' done!'
        with open(r'..\ProductURLData\breakpoint.txt', 'w') as f:
            f.write(str(i))

if __name__ == '__main__':
    with open(r'..\ProductURLData\breakpoint.txt', 'r') as f:
        breakpoint = f.readline()
    breakpoint = int(breakpoint)
    getProductURL(breakpoint)







