
import requests
from bs4 import BeautifulSoup
import re
import sys

def getLaptopPage():

	for x in range(1,1071):
		LapUrl = "https://list.jd.com/list.html?cat=670,671,672&page=%s&sort=sort_totalsales15_desc&trans=1&JL=6_0_0&ms=6#J_main"% str(x)
		res_str = requests.get(LapUrl).text
		getLabtop(res_str)




def getLabtop(res_str):
	productIds = []
	soup = 	BeautifulSoup(res_str,"html.parser")
	productTemps = soup.select('.gl-i-wrap')
	for productTemp in productTemps:
		productId = productTemp.attrs['data-sku']
		getLabtopComments(productId)
	# return productIds



def getLabtopComments(productId):
	

	f = open("comments.txt",'w',1)
	for x in range(0,2000):
		commentUrl = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6736&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1"%(productId,str(x))
		res = requests.get(commentUrl)
		pattern_get = re.compile(r'creationTime')
		
		if pattern_get.search(res.text) != None:
			comments = eval(res.text[26:-2].replace('null', 'None').replace('false', 'False').replace('true', 'True'))
			for c in comments['comments']:
                                # print c['content']
                                f.write("".join(c['content']))
                                f.write("\n-----------------------------\n")
			
		else :
			break
	f.close()

#-*- coding:utf-8 -*-

def main():
	print("start")
	getLabtopComments(12966195053)
	print("finished")
	return 

if __name__ == '__main__':
	main()