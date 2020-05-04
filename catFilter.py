# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:49:42 2020

@author: Web
"""

import pandas as pd
import numpy as np
df = pd.read_pickle('mergedDf')
cats = df.groupby('CAT').nunique().UPC.sort_values().rename('num_unique')
df = pd.merge(df,cats, on='CAT', how='left')
# df.CAT = np.where(df.num_unique < 12, 'Miscellaneous', df.CAT)

# df.to_pickle('mergedDf')






# c = pd.Series(sorted(df.CAT.astype(str).unique()))
# cats = c.str.split('/', expand=True)
# cats.columns=list('abcx')
# cats = cats.merge(c.rename('CAT'), \
#                   left_index=True, right_index=True)[['CAT','a','b','c']]
# df = df.join(cats.set_index('CAT'), on='CAT', how='left')
# gb = df
# .groupby(list('abc'))
# info = gb.nunique()

# """
# array(['Disc Golf', 'Electronic', 'Eyewear', 'FBA', 'Headwear', 'Hike',
#        'Kayak', 'Lifejacket', 'Mens', 'Race', 'Safety', 'Service',
#        'Skateboard', 'Ski', 'Snowboard', 'Stupid', 'Wakeboard',
#        'Watersport', 'Winter', 'Womens', 'Youth'], dtype=object)

# cats.b.unique()
# Out[303]: 
# array(['Bag', 'Audio', 'Goggles', 'Sunglasses', 'Bindings', 'Board',
#        'Beanie', 'Facemask', 'Hat', 'Pack', 'Accessory', 'Neoprene',
#        'Nylon', 'Baselayer', 'Lifestyle', 'Midlayer', 'Outerwear',
#        'Swimwear', 'Night', 'Avalanche', 'Helmet', 'Pad', 'Race', 'Ski',
#        'Bearings', 'Complete', 'Completes', 'Deck', 'Griptape',
#        'Hardware', 'Shoes', 'Trucks', 'Wheels', 'Bags', 'Boots', 'Poles',
#        'Skis', 'Socks', 'Tune', 'Tuning', 'X-Country', 'Accessorie',
#        'Misc', 'Packages', 'Surf', 'Wakeskate', 'Wakesurfs', 'Kneeboard',
#        'Rashguard', 'SUP', 'Towable', 'Wetsuit', 'Equipment'],
#       dtype=object)

# cats.c.unique()
# Out[304]: 
# array([None, 'Accessory', 'Moto', 'Rep. Lens', 'Unisex', 'Womens',
#        'Youth', 'Hydration', 'Map', 'Mens', 'Snow', 'Dog', 'Men',
#        'Bottom', 'Suit', 'Top', 'Bag', 'Jacket', 'Pants', 'Shoes',
#        'Shorts', 'Gloves', 'Jackets', 'Mittens', 'Probe', 'Shovel',
#        'Tranceiver', 'Skate', 'Ski', 'Wakeboard', 'BindngPart', 'Brakes',
#        'Tune', 'Street', 'Long Board', 'Longboard', 'Insoles', 'Backpack',
#        'Boot', 'Gear', 'Liner', 'Parts', 'Adult', 'Baskets', 'Wax',
#        'Tool', 'Boots', 'Skis', 'StompPads', 'Board Bag', 'Travel',
#        'Wheel', 'Women', 'Crap', 'Board', 'Combo', 'Handle', 'Single',
#        'Tube', 'Dress', 'Jumpsuit'], dtype=object)
# """