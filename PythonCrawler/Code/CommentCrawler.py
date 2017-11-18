#encoding: utf-8

import json
import codecs

class CommentCrawler(object):


    def __init__(self, html, productID):
        s = html[27: -2]
        try:
            comments = json.loads(s)
        except ValueError, e:
            print "ValueError"
            return
        self.__comments = comments
        self.__productID = productID
        self.__flag = 0

    @property
    def comments(self):
        return self.__comments

    @property
    def getCommentsContent(self):
        contents = []
        for i in self.__comments['comments']:
            contents.append(i['content'])

    @property
    def getCommentsTime(self):
        times = []
        for i in self.__comments['comments']:
            times.append(i['creationTime'])

    @property
    def getCommentsScore(self):
        scores = []
        for i in self.__comments['comments']:
            scores.append(i['score'])

    @property
    def getCommentsUsefulCount(self):
        usefulVoteCount = []
        for i in self.__comments['comments']:
            usefulVoteCount.append(i['usefulVoteCount'])

    @property
    def getCommentsConfig(self):
        config = []
        for i in self.__comments['comments']:
            config.append(i['productColor'] + i['productSize'])

    def writeComments(self, folder_path):
        with codecs.open(folder_path + "/reviews.txt", 'a', encoding='utf-8') as f:
            for comment in self.comments['comments']:
                f.write(comment['content'])
                f.write('\r\n')
                f.write('Score: ' + str(comment['score']))
                f.write('\r\n')
                f.write('CreationTime: ' + comment['creationTime'])
                f.write('\r\n')
                f.write('UsefulVoteCount: ' + str(comment['usefulVoteCount']))
                f.write('\r\n')
                f.write('ProductType: ' + comment['productColor'] + '  ' + comment['productSize'])
                f.write('\r\n')
                f.write('-------------------------------------------------------------------------------------------------------------------------------------------------------------' + '\r\n')


    # def __detectError(self):
    #     if len(self.__comments) == 0:
    #         with open(r'../Data/errorID.txt', 'a') as f2:
    #             f2.write(str(self.__productID) + 'value error!' + '\n')



