# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:30:09 2020

@author: robbi
"""
#%%
#import
import numpy as np
import pandas as pd


data = pd.read_csv('magento04302020.csv',\
                 low_memory= False)\
    .dropna(axis= 1, how= 'all')

cols= [\
          'related_parent_id',\
          'related_id',\
          'upc',\
          # 'image',\
          'size',\
          'color',\
          'description',\
          'short_description',\
          
      ]\

dfImg = pd.DataFrame(data, columns= cols)
#%%
#upc
dfImg.upc = dfImg.upc\
    .fillna(0)\
    .astype(str)\
    .str.replace(r'\.0$','',regex= True)
def makeN(x, n):
    if len(x) == n:
        return x
    else:
        return '0'*(n-len(x)) + x
dfImg.upc = dfImg.upc.apply(lambda x: makeN(x,13))\
    .map(lambda x: np.nan if x == '0'*13 else x)

#%%

# dfImg.image = dfImg.image\
#     .map(lambda x: np.nan if x == 'no_selection' else x)
# dfImg.image = 'product' + dfImg.image


#%%

#joining
# df = pd.read_pickle('fromRetailPro')
# bigDf = pd.merge(df,dfImg,left_on= 'UPC',right_on= 'upc', how='left')


# #joining on multindex

# dfImg.set_index(['related_parent_id','related_id'], inplace=True)
# dfImg.sort_index(inplace=True)
# dfImg.index.rename(['a','b'], inplace=True)
# dfImg = dfImg.loc[dfImg.index.dropna()]
    
# df = pd.read_pickle('x')
# df.drop_duplicates(subset='itemSID', keep='first', inplace=True)
# df.set_index(['styleSID','itemSID'], inplace= True)
# df.sort_index(inplace=True)
# df.index.rename(['a','b'], inplace=True)

# #BIG LIMITER, CONSIDER LEFT JOIN
# bigDf = pd.merge(df,dfImg, left_index=True, right_index=True, how='outer')\
#     .dropna(axis= 1, how = 'all')


#%%
#filters
#bigDf = bigDf.loc[bigDf.image.notnull()]



#%%
#pickle
dfImg.to_pickle('fromMagento')



























"""color map"""
# x = bigDf.loc[(bigDf.size_x != bigDf.size_y) | (bigDf.color_x != bigDf.color_y)]\
#     [['size_x','size_y','color_x','color_y']]\
#     .dropna(how='all')

# def count_unique_index(df, by):                                                                                                                                                 
#     return df.groupby(by).size().reset_index().rename(columns={0:'count'})
# y = count_unique_index(bigDf[['color_x','color_y']],['color_x','color_y'])
# z = y.loc[y.color_x != y.color_y][['color_x','color_y']].set_index('color_x')

# colorMap = z.to_dict()



