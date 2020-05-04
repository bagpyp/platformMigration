# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:43:07 2020

@author: robbi
"""

import pandas as pd
import datetime as dt
import numpy as np

#%%
#merge

df1 = pd.read_pickle('fromRetailPro')
df2 = pd.read_pickle('fromMagento')
df2.columns = ['styleSID','itemSID','UPC',\
               # 'image_0',\
               'size','color','desc','desc_short']
df2 = df2[df2.styleSID.notnull()]
df3 = pd.read_pickle('fromRDI')


x = pd.merge(df1,df2, on='UPC',how='left')
df3.rename(columns={'styleSID':'styleSID_x','color':'color_x'},\
           inplace=True)
y = x.set_index(['styleSID_x','color_x']).join(\
            df3.set_index(['styleSID_x','color_x']),\
                how= 'left').reset_index()
    
cols=['sku',\
    'styleSID_x',\
    'styleSID_y',\
    'itemSID_x',\
    'itemSID_y',\
    'name',\
    'year',\
    'color_x',\
    'color_y',\
    'size_x',\
    'size_y',\
    'UPC',\
    'image',\
    # 'image_0',\
    'image_1',\
    'image_2',\
    'image_3',\
    'image_4',\
    'desc',\
    'desc_short',\
    'CAT',\
    'BRAND',\
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
    'descriptionA',\
    'imageA']
    
df=y[cols]

# df.image = np.where(df.image.isnull(),df.image_0,df.image)

df.loc[:,['color_x','size_x','color_y','size_y']]\
    = df[['color_x','size_x','color_y','size_y']].replace('',np.nan)
    
df.loc[:,'color'] = np.where(df.color_y.notnull() & df.color_x.notnull(),\
                          df.color_y,\
                          df.color_x)

df.loc[:,'size'] = np.where(df.size_x.notnull() & df.size_y.notnull(),\
                         df.size_y,\
                         df.size_x)
    
df.drop(['styleSID_y','itemSID_y',\
         'color_x','color_y',\
         'size_x','size_y'],\
        axis= 1,\
        inplace=True)
    
df.rename(columns={'styleSID_x':'styleSID','itemSID_x':'itemSID'},\
           inplace=True)
    
df['webName'] = (df.name + ' ' + df.year.fillna('')).str.strip()

#%%
#settle distinct webName vs. styleSIDs, v complicated
webDf = df 
gb = webDf.groupby('webName')   
l = []
for (a,g) in gb:
    if g.styleSID.nunique() > 1:
        for i in range(1,g.styleSID.nunique()):
            l.extend(g[(g.styleSID == g.styleSID.unique()[i])]\
            .index.to_list())
        
webDf.drop(index=l,inplace=True)
# webDf =  webDf[webDf.sku!='002956']

"""uncomment to run outside of main"""
# webDf.to_pickle('mergedDf')

