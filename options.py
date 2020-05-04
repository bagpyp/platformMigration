# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:48:01 2020

@author: web
"""

import pandas as pd
import numpy as np
df = pd.read_pickle('mergedDf')
df['itemType']='Product'
df.rename(columns= {'size':'size_'}, inplace=True)

gb = df.groupby('webName')
"""
x = pd.concat([gb.size(),gb.first()], axis=1).reset_index()
x.rename(columns={0:'a'})
x.groupby('a').first().webName.to_list()
"""
#each group is of some unique size
#consider AB testing wiht gb.last() as well
gps = ['10 Scraper 19-20',
 '#Meowtains 18-19',
 '18oz Wide Mouth',
 '11.0 TP 18-19',
 'AM 12 19-20',
 '3Feet High 19-20',
 '40oz Wide Mouth',
 'AMT 19-20',
 'Blin 19-20',
 'AMT Boy 19-20',
 'Canuk 19-20',
 'Anthem 19-20',
 'Maysis 19-20',
 'Cloud W 19-20',
 'Faction Boa 19-20',
 'Arctic Pole 19-20',
 'Anthem 18-19',
 'Maze 19-20',
 'Cargo Mid 18-19',
 '540 P-Lite 19-20',
 'Seymore Pant 18-19',
 'Lasso 18-19',
 'FDGB 18-19',
 'Sally Pant 18-19']
# samples = [gb.get_group(name) for name in gps]
# sample = pd.concat(samples[:10])
# gb = sample.groupby('webName')


"""for making rt adn rbs"""
#f'[RT]Color={color}'
#f'[RB]Size={size}
def ops(df):
    ops = df.webName
    if pd.notnull(df.color) and pd.notnull(df.size_):
        ops = f'[RT]Color={df.color}'+','+f'[RB]Size={df.size_}'
    elif pd.notnull(df.size_) and pd.isnull(df.color):
        ops = f'[RB]Size={df.size_}'
    elif pd.notnull(df.color) and pd.isnull(df.size_):
        ops = f'[RT]Color={df.color}'
    return ops



def add_row(x):
    if len(x.index) > 1:
        #fr = first row of x
        """header"""
        fr = x.iloc[0]
        if x. image.notnull().sum():
            fr.image = x.image.loc[x.image.first_valid_index()]
        fr.color = fr['size'] = np.nan
        fr.pSale = x.pSale.min()
        fr.sku = '0-' + fr.sku
        fr.cost = x.cost.max()
        x = x.append(fr).sort_values('sku')
        """SKUs"""
        y = x.iloc[1:,:].copy()
        y.itemType = 'SKU'
        y.webName = y.apply(lambda x: ops(x),axis=1)
        y.sku = '1-'+y.sku
        y.cost 
        """RULES"""
        z = x.iloc[1:,:].copy()
        z.itemType = 'Rule'
        z.pSale = '[FIXED]' + z.pSale.astype(str)
        z.sku = '1-'+z.sku        
        x = x.iloc[[0]].append(y)
        x = x.append(z)
    return x

sample_out = gb.apply(add_row)


# prePre = gb.get_group('11.0 TP 18-19')
# pre = sample_in.iloc[6:10,:].dropna(axis=1,how='all')
# post = sample_in.iloc[11:20,:].dropna(axis=1,how='all')

sample_out.to_pickle('optionDf')






























