# -*- coding: utf-8 -*-

import os
import pandas as pd
from BasicCrawler import BasicCrawler
from CommentCrawler import CommentCrawler
from ConfigCrawler import ConfigCrawler

if __name__ == '__main__':
    with open(r'../Data/breakpoint.txt', 'r') as f:
        breakpoint = f.readline()
    breakpoint = int(breakpoint)
    with open(r'../Data/pageNum.txt', 'r') as f:
        pageNum = f.readline()
    pageNum = int(pageNum)
    data = pd.read_csv(r'../ProductURLData/productID.csv')
    productName = data['Name']
    productID = data['ID']
    breakpoint_record = data['breakpoint']
    basic_crawler = BasicCrawler()
    while True:
        for i in range(breakpoint, breakpoint + 1):
            folder_path = r'../Data/' + productID[i]
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            config_crawler = ConfigCrawler(basic_crawler.getHTML('https://item.jd.com/' + productID[i] + '.html#product-detail'), productID[i], productName[i])
            config_crawler.writeConfig(folder_path)
            for pageNum in range(pageNum, 500):
                # try:
                comment_crawler = CommentCrawler(basic_crawler.getHTML(basic_crawler.getURL(pageNum, productID[i])), productID[i])
                # except Exception, e:
                #     print i
                #     print productID[i].encode('utf-8') + ' ' + str(pageNum) + 'get_html error!'
                #     basic_crawler.recordError(productID, 'get html error')
                # try:
                comment_crawler.writeComments(folder_path)
                # except Exception, e:
                # print "write comments error"
                # break
                with open(r'../Data/pageNum.txt', 'w') as f:
                    f.write(str(pageNum))
            with open(r'../Data/breakpoint.txt', 'w') as f:
                f.write(str(i))
            pageNum = 0
        breakpoint += 1



    
