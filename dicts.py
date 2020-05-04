# -*- coding: utf-8 -*-

import pandas as pd

data = pd.read_excel('DCScats.xlsx')
df = pd.DataFrame(data)

df = df.fillna('')

df.Dn = df.Dn.str.strip()
df.Cn = df.Cn.str.strip()
df.Sn = df.Sn.str.strip()

df['CAT']= df.Dn + '/' + df.Cn + '/' + df.Sn

def killTrailingSlash(x):
    if x[-1] == '/':
        x = x[:len(x)-1]
    return x

df.DCS = df.DCS.str.strip()
df.CAT = df.CAT.apply(killTrailingSlash)

df.to_pickle('cats')


df2 = pd.read_excel('VCvends.xlsx')
df2 = df2.fillna('')


df2["Vend Code"] = df2["Vend Code"].str.strip()
df2["Company"] = df2["Company"].str.strip()

df2.to_pickle('vends')

