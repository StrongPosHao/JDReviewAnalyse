#encoding: utf-8

import requests
from bs4 import BeautifulSoup
from BasicCrawler import BasicCrawler

class ConfigCrawler(object):

    def __init__(self, html, productID, productName):
        self.__soup = BeautifulSoup(html, 'html.parser')
        self.__Item = self.__soup.find('div', class_="Ptable")
        self.__productID = productID
        self.__productName = productName

    def writeConfig(self, folder_path):
        with open(folder_path + '/basicInfo.txt', 'w') as f:
            f.write(self.__productName + '\n' * 2)
            try:
                print 'OK' + self.__productID
                for j in self.__Item.find_all('div', class_="Ptable-item"):
                    f.write(j.h3.string.encode('utf-8').strip() + "\n\n")
                    for k, h in zip(j.dl.find_all('dt'), j.dl.find_all('dd')):
                        f.write(k.string.encode('utf-8') + ": " + h.string.encode('utf-8') + '\n')
                    f.write('\n' * 4)
            except Exception, e:
                print self.__productID + '      getBasicInfoError'
                with open(r'../Data/errorID.txt', 'a') as f2:
                    f2.write(str(self.__productID) + '  get_basicinfo error!' + '\n')
                print 'OK' + self.__productID
                for j in self.__Item.find_all('div', class_="Ptable-item"):
                    f.write(j.h3.string.encode('utf-8').strip() + "\n\n")
                    for k, h in zip(j.dl.find_all('dt'), j.dl.find_all('dd')):
                        f.write(k.string.encode('utf-8') + ": " + h.string.encode('utf-8') + '\n')
                    f.write('\n' * 4)
            except Exception, e:
                print self.__productID + '      getBasicInfoError'
                with open(r'../Data/errorID.txt', 'a') as f2:
                    f2.write(str(self.__productID) + '  get_basicinfo error!' + '\n')