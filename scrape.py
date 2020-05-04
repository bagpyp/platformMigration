# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:53:50 2020

@author: Web
"""


import pandas as pd
df = pd.read_pickle('fromRetailPro')
sample = df[(df.qty>0) & (df.lSold > '04/13/2019')]

# outF = open('outFile.txt','w')

# for upc in sample.UPC:
#     outF.write(upc)
#     outF.write('\n')
# outF.close()
    
"""ran octoparse"""

dfOP = pd.read_excel('fromOctoparse.xlsx')
dfOP.columns = ['imageA','desc1','descriptionA','desc2','UPC']
def makeN(x, n):
    if len(x) == n:
        return x
    else:
        return '0'*(n-len(x)) + x


dfOP.UPC = dfOP.UPC.astype(str).fillna('0'*13).apply(lambda x: makeN(x,13))

df = pd.merge(df,dfOP,how='left',left_on='UPC',right_on='UPC')

df.to_pickle('fromRetailPro')