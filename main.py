# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:41:43 2020

@author: Web
"""
import os
from spydercustomize import runfile
import numpy as np
import datetime as dt


"""
Make sure contents of R:\Retail8\Rpro\IMAGES\INVEN have been uploaded to 
CyberDuck, taking care to skip duplicates when mass uploading

Make Sure the Magento export has been replaced by the most current CSV from 
https://www.hillcrestsports.com/index.php/hillcres_admin/
dashboard/index/key/b426e581794e6dd135fd1e195e3187be/
System>Import/Export>Esport as csv, not checking anything

Make sure to have run EXP_INVEN from the ~BRIDGE.EXE program on the
desktop of WS1, which should overwrite the CSV file at 'R:\ECIEXP\ECIINV.CSV'
To run, choose Run Map, press 'F' for Find, type 'E' to locate map: EXP_INVEN

If there have been any category or brand updates in Retail Pro, export the 
Vendor and Category lits to excel and format columns per dicts.py

Don't try and fuck eith the octoparse stuff, that was a one time deal.  There
might actually be some valuable info in the excel sheets that we can look into
exploiting later tho...


"""

cwd = os.getcwd()


#run 
if __name__ == '__main__':
    
    
    
    print('loading brand and category dicts from excel files')
    runfile(cwd + '\\' + 'dicts.py', \
            wdir=cwd)
        
        
    """comment out on local machine"""
    # print('running from Retail Pro ~BRIDGE')
    # runfile(cwd + '\\' + 'dataPrep.py', \
    #         wdir=cwd)
    
    
    
    print('running from Magento CSV Export')
    runfile(cwd + '\\' + 'magento.py', \
            wdir=cwd)
        
        
    """comment out on local machine"""
    # print('running from RDi INVEN/IMAGES')
    # runfile(cwd + '\\' + 'fromRpro.py', \
    #         wdir=cwd)
    
    
    
    print('running from Octoparse scraping data')
    runfile(cwd + '\\' + 'scrape.py', \
            wdir=cwd)
    
        
    print('merging dataframes')
    runfile(cwd + '\\' + 'merge.py', \
            wdir=cwd)
    
        
        
    from merge import webDf
    """filtering and tuning descriptions"""

    df = webDf.loc[(webDf.qty>0) | \
                   (webDf.lSold > (dt.datetime.now() \
                                   - dt.timedelta(days=1*365)))]



    
    df.desc = np.where(df.desc.isnull(),df.desc_short,df.desc)
    df.desc = np.where(df.desc.isnull(),df.descriptionA,df.desc)


    df.to_pickle('mergedDf')
    
    # """filtering CATS"""
    # # consider filetering out instead of df
    # print('sending to CAT filter')
    # runfile(cwd + '\\' + 'catFilter.py', \
    #         wdir=cwd)

    
    #%%
    print('***********configuring product options, please hold************'\
          .upper())
    runfile(cwd + '\\' + 'options.py', \
            wdir=cwd)
    
    print('preparing bigCommerce upload file df as "out"')
    
    # runfile(cwd + '\\' + 'excelPrep.py', \
    #         wdir=cwd)
    
    from excelPrep import out
    out.to_csv('upload.csv', quotechar="\"")
    
    
