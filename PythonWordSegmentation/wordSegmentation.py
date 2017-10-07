# -*- coding: utf-8 -*-

import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


inpath = "../PythonCrawler/ReviewsData/comments.txt"
outpath = "./Jcomments.txt"
def wordSegmentation():
    
    comments = []
    content = open(inpath, 'r').read()
    temps = content.split("----------------------------------------------------------------------------------------------------------")
    for temp in temps:
        comments.append(temp)

    comments = "".join(comments)
    jieba.suggest_freq("暗影精灵",True)
    jieba.suggest_freq("拯救者",True)
    seg_list = jieba.cut(comments,HMM=True)
    File = open(outpath,'w').write("/".join(seg_list))
    
    

    

if __name__ == '__main__':
    wordSegmentation()
    print'OK'
