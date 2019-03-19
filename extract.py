# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 21:55:13 2019

@author: Aniruddha choudhury
"""
import requests 
import xml.etree.ElementTree as ET 
import urllib
import urllib.request
import pandas as pd
with urllib.request.urlopen("https://www.sec.gov/Archives/edgar/data/72971/000007297117000278/wfc-20161231.xml") as url:
    s = url.read()
#I'm guessing this would output the html source code?
print(s)


f = open('route3044.xml', 'wb')
f.write(s)
f.close()

xmlfile='route3044.xml'
tree = ET.parse(xmlfile) 


# get root element 
root = tree.getroot() 
root.tag
root.attrib

l=list()
r=list()
for child in root:
    l.append(child.tag)
    r.append(child.text)
    print (child.tag, child.text)
    
x=pd.DataFrame(l)
y=pd.DataFrame(r)
data=pd.concat([x,y],axis=1,ignore_index=True)
data1=data.dropna(axis=0, subset=[0])



data.columns=['a','b']

to_drop=["<div"]
data1=data[~data['a'].str.contains("{http://www.xbrl.org/2003/instance}context")]
data1=data1.dropna()
data1=data1[~data1['b'].str.match('<div')]
data1=data1[~data1['a'].str.contains("{http://www.xbrl.org/2003/instance}unit")]


data1=data1.reset_index()
del data1['index']


def reset(A):
    A=A.reset_index()
    del A['index']
    return A


data_new1=data1[data1['a'].str.contains("{http://xbrl.sec.gov/dei/2014-01-31}")]
data_new1['Entity'] = data_new1['a'].str.split('{http://xbrl.sec.gov/dei/').str[1]
del data_new1['a']
data_new1['date'] = data_new1['Entity'].str.split('}').str[0]
data_new1['attributes'] = data_new1['Entity'].str.split('}').str[1]
del data_new1['Entity']

data_new1=reset(data_new1)



data_new2=data1[data1['a'].str.contains("{http://xbrl.sec.gov/invest/2013-01-31}")]
data_new2['Entity'] = data_new2['a'].str.split('{http://xbrl.sec.gov/invest/').str[1]
del data_new2['a']
data_new2['date'] = data_new2['Entity'].str.split('}').str[0]
data_new2['attributes'] = data_new2['Entity'].str.split('}').str[1]
del data_new2['Entity']

data_new2=reset(data_new2)


data_new3=data1[data1['a'].str.contains("{http://fasb.org/us-gaap/2016-01-31}")]
data_new3['Entity'] = data_new3['a'].str.split('{http://fasb.org/us-gaap/').str[1]
del data_new3['a']
data_new3['date'] = data_new3['Entity'].str.split('}').str[0]
data_new3['attributes'] = data_new3['Entity'].str.split('}').str[1]
del data_new3['Entity']

data_new3=reset(data_new3)


data_new4=data1[data1['a'].str.contains("{http://www.wellsfargo.com/20161231}")]
data_new4['Entity'] = data_new4['a'].str.split('{http://www.wellsfargo.com/').str[1]
del data_new4['a']
data_new4['date'] = data_new4['Entity'].str.split('}').str[0]
data_new4['attributes'] = data_new4['Entity'].str.split('}').str[1]
del data_new4['Entity']


data_new4=reset(data_new4)


D=[data_new1,data_new2,data_new3,data_new4]
newtable=pd.concat(D)

cols=list(newtable)
cols.insert(0,cols.pop(cols.index('attributes')))
newtable=newtable.ix[:,cols]
newtable=newtable.reset_index()

del newtable['index']


del data1['text_new']
data1['text_new'] = data1['a'].str.split('{http://xbrl.sec.gov/dei/').str[1]

newtable.columns=['Attributes','Values','Data']

newtable.to_csv('final.csv',index=False)








    