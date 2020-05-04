# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
df = pd.read_pickle('optionDf').reset_index(drop=True)






data = pd.read_csv('uploadTemplateOriginal.csv')
cols = list(data.columns)
out = pd.DataFrame(columns = cols)

"""
Item Type
Product ID
Product Name
Product Type
Product Code/SKU
Bin Picking Number
Brand Name
Option Set
Option Set Align
Product Description
Price
Cost Price
Retail Price
Sale Price
Fixed Shipping Cost
Free Shipping
Product Warranty
Product Weight
Product Width
Product Height
Product Depth
Allow Purchases?
Product Visible?
Product Availability
Track Inventory
Current Stock Level
Low Stock Level
Category
Product Image ID - 1
Product Image File - 1
Product Image Description - 1
Product Image Is Thumbnail - 1
Product Image Sort - 1
Product Image ID - 2
Product Image File - 2
Product Image Description - 2
Product Image Is Thumbnail - 2
Product Image Sort - 2
Search Keywords
Page Title
Meta Keywords
Meta Description
MYOB Asset Acct
MYOB Income Acct
MYOB Expense Acct
Product Condition
Show Product Condition?
Event Date Required?
Event Date Name
Event Date Is Limited?
Event Date Start Date
Event Date End Date
Sort Order
Product Tax Class
Product UPC/EAN
Stop Processing Rules
Product URL
Redirect Old URL?
GPS Global Trade Item Number
GPS Manufacturer Part Number
GPS Gender
GPS Age Group
GPS Color
GPS Size
GPS Material
GPS Pattern
GPS Item Group ID
GPS Category
GPS Enabled
"""

#monies
out["Cost Price"] = df["cost"]
out["Retail Price"] = df["pMSRP"]
out["Sale Price"] = df["pSale"]

#name
out["Product Name"] = df.webName

#images
    #needs descriptions
out["Product Image File - 1"] = df.image
out[[f'Product Image File - {i+1}' for i in range(1,5)]]\
    = df[[f'image_{i}' for i in range(1,5)]]
out = out.reindex(out.columns.to_list()\
                  +[f"Product Image ID - {i}" for i in range(3,6)]\
                  +[f'Product Image Description - {i}' for i in range(3,6)],\
                      axis=1)

#descriptions
out['Product Description'] = df.desc

out["Brand Name"] = df.BRAND









out["Current Stock Level"] = df.qty
out["Product Code/SKU"] = df.sku
out["Product UPC/EAN"] = df.UPC
# out["Product Custom Fields"] = df.PCF

out["Product Weight"] = df.weight
# out["Product URL"] = df.url_path


#defaults

out["Allow Purchases?"] = 'Y'
out["Item Type"] = df.itemType
out["Product Type"] = 'P'
out["Track Inventory"] = np.where(df.sku.str[:2]=='1-',\
                                  'by option','by product')
    
    
df['PV'] = np.where(((df.image.isnull()) | (df.qty==0)),\
                                   'N','Y')
out['Product Visible?'] = df.PV


    
    
categoryFilter= False
if categoryFilter:    
        
    """categories"""
    
    cats = df.loc[df.PV=='Y'].groupby('CAT').UPC.nunique().rename('num_unique')
    x = pd.merge(df,cats, on='CAT', how='left')
    x.CAT = np.where(x.num_unique < 9, 'Miscellaneous', x.CAT)
    
    out["Category"] = x.CAT
else:
    out["Catgory"] = df.CAT

#drop na



"""uncomment to run outside of main"""
# out.to_csv('upload.csv', quotechar="\"")

