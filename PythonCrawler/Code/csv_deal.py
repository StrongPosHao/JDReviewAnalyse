#encoding: utf-8

import pandas as pd
from pandas import DataFrame

def deal_csv():
    data = pd.read_csv(r'../ProductURLData/URL.csv')
    url_data = data['URL']
    name_data = data['Name']
    count = 1
    with open(r'../ProductURLData/productID.txt', 'a') as f:
        for i in url_data:
            f.write(i[20:-5] + ',' + str(count) + '\n')
            count += 1

if __name__ == '__main__':
    deal_csv()
