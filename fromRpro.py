# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:43:15 2020

@author: robbi
"""

import pandas as pd
import numpy as np
from glob import glob

fnames = []
fnames_thumb = []
path = r'R:\Retail8\Rpro\IMAGES\INVEN\*'
for fname in glob(path):
    if '__S' in fname:
        fnames_thumb.append(fname[len(path)-1:])
    else:
        fnames.append(fname[len(path)-1:])    
#one file is named PAGGABBGKHDPCCDM_P.Blue_1.jpg
fnames.remove('PAGGABBGKHDPCCDM_P.Blue_1.jpg')

#%%
"""large images"""
ser = pd.Series(fnames, name='e')
ser = ser[ser.str.match(r'^[A-Z]{13}')]
df = pd.concat([\
                   ser.apply(lambda x: x[:16]),\
                   ser],\
               axis= 1)
df.columns = ['styleSID','image']

df[['imageName','extension']] = df.image.str.split('.', expand= True)
df[['color','num']] = df.imageName.str.split('_', expand=True).iloc[:,[1,2]]
df.color = df.color.fillna('')
df = df.set_index(['styleSID','color'])
df.drop(['imageName','extension'], axis= 1, inplace= True)
gb = df.groupby(['styleSID','color'])
df = pd.DataFrame(index= df.index.unique())
for i in range(5):
    df = df.join(gb.nth(i).image, how='left', rsuffix= f'_{i}')

x = df.reset_index()


#%%
"""thumbs"""

df = pd.DataFrame(fnames_thumb,columns=['image'])
df = df.join(\
        df.image.str.replace('__S','')\
        .str.split('.',expand= True)\
        .iloc[:,0]\
        .str.split('_',expand=True)\
        .rename(axis=1,\
                mapper={0:'styleSID',1:'num'}))\
                        [['styleSID','num','image']]
                        
gb = df.groupby('styleSID')
df = pd.DataFrame(index=df.styleSID.unique())
for i in range(3):
    df = df.join(gb.nth(i).image, how='left',rsuffix= f'_{i}')
df.columns= [f'image_{i+1}' for i in range(3)]

df = x.join(df, on='styleSID', rsuffix='_X')
for i in range(1,4):
    df[f'image_{i}'] = np.where(df[f'image_{i}'].isnull(),\
                                df[f'image_{i}_X'],\
                                df[f'image_{i}'])
        
df = df[df.columns[:7]]


#%%
df.to_pickle('fromRDI')
