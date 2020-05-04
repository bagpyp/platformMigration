# -*- coding: utf-8 -*-
"""
main
"""
#%%
import pandas as pd
from csv import QUOTE_NONE as qn
import numpy as np


""" data """

#read in
df = pd.read_csv(r'R:\ECIEXP\ECIINV.CSV',\
                    encoding = 'ansi',\
                    quoting= qn,\
                    index_col = False,\
                    names = ['sku',\
                              'aux0',\
                              'aux1',\
                              'aux2',\
                              'aux3',\
                              'name',\
                              'year',\
                              'color',\
                              'd3',\
                              'weight',\
                              'qty1',\
                              'qty2',\
                              'itemSID',\
                              'size',\
                              'pSale',\
                              'pMSRP',\
                              'pMAP',\
                              'pAmazon',\
                              'pSWAP',\
                              'DCS',\
                              'UPC',\
                              'VC',\
                              'lRcvd',\
                              'lSold',\
                              'fRcvd',\
                              'lEditD',\
                              'lEditT',\
                              'cost',\
                              'styleSID'],\
                    # dtype = {'sku':str,\
                    #          'upc':str}\
                        )\
    .drop(['aux0','aux1','aux2','aux3','d3'], axis=1)\
    .replace(r"\"","",regex= True)
#%%
#filters
df.replace(r'\"','',regex= True, inplace=True)
df = df[df.styleSID.str.match(r'^[A-Z]{16}$')]
df = df[df.DCS.str.match(r'^((?!USD|REN).)*$')]
df = df[df.UPC.notnull()]
# df = df.set_index('itemSID')



"""dtypes"""
#%%
#ints
def convert(s):
    if '-' in s:
        return float(s[-1:] + s[:-4])
    return float(s)
df.qty1 = df.qty1.apply(convert).map(int)
df.qty2 = df.qty2.apply(convert).map(int)
#%%
#floats                 
df[['cost','pSale','pMSRP','pMAP','pAmazon']]\
    = df[['cost','pSale','pMSRP','pMAP','pAmazon']].apply(pd.to_numeric)
#%%
#dates
df[['lRcvd', 'lSold', 'fRcvd']]\
    = pd.to_datetime(\
                     df[['lRcvd', 'lSold', 'fRcvd']]\
                         .astype(str)\
                         .stack(),\
                     format = '%y%m%d',\
                     errors = 'coerce'\
                     ).unstack()
#%%
#datetime
df.lEditT = df.lEditT.str.replace(r'\.\d\d$','',regex= True)
df["lEdit"]\
    = pd.to_datetime(\
                      df['lEditD'].astype(str)\
                          + df['lEditT'],\
                    format = '%y%m%d%H:%M',\
                    errors = 'coerce')
df = df.drop(['lEditT','lEditD'], axis= 1)
#%%               
#skus and upcs
def makeN(x, n):
    if len(x) == n:
        return x
    else:
        return '0'*(n-len(x)) + x


df.UPC = df.UPC.fillna('0'*13).apply(lambda x: makeN(x,13))
df.sku = df.sku.astype(str).fillna('0'*6).apply(lambda x: makeN(x,6))

#%%   
#add category column
df.DCS = df.DCS.str.strip()
df["CAT"] = df.DCS.map(\
                       dict(pd.read_pickle('cats')[["DCS","CAT"]].values)\
                           ).astype('category')
#add brands column
df.VC = df.VC.str.strip()
df["BRAND"] = df.VC.replace(\
                        dict(pd.read_pickle('vends').values)\
                            ).astype('category')
#%%
#weights
df.weight\
    = df.weight.str.replace('lbs','')\
    .apply(pd.to_numeric, errors='coerce')\
    .fillna(0)

#qty column
df["qty"] = df.qty1 + df.qty2

#%%
# #nans, color adn size, fucks merge in fromRpro
# df[['color','size']] = df[['color','size']].replace('',np.nan)
#%%
#reorder
cols = [\
        'sku',\
        'UPC',\
        'styleSID',\
        'itemSID',\
        'CAT',\
        'BRAND',\
        'name',\
        'year',\
        'color',\
        'size',\
        'weight',\
        'qty',\
        'cost',\
        'pSale',\
        'pMSRP',\
        'pMAP',\
        'pAmazon',\
        'pSWAP',\
        'fRcvd',\
        'lRcvd',\
        'lSold',\
        'lEdit',\
        ]

df = df[cols]

#%%
#pickle
df.to_pickle('fromRetailPro')

