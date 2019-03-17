import csv 
import requests 
import xml.etree.ElementTree as ET 
import urllib
import urllib.request
with urllib.request.urlopen("https://datafied.api.edgar-online.com/v2/corefinancials/ann.xml?primarysymbols=wfc&numperiods=6&appkey=f1d1a0122cc467c799c1b3529e634e15") as url:
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



news={}
for child in root:
    print (child.tag, child.text)
    news[child.tag] = child.text.encode('utf8')


from xml.dom import minidom
xmldoc = minidom.parse('route3044.xml')
itemlist = xmldoc.getElementsByTagName('value') 
print ("Len : ", len(itemlist))
print ("Attribute Name : ", itemlist[0].attributes['field'].value)
print ("Text : ", itemlist[0].firstChild.nodeValue)

q=list()
m=list()
for s in itemlist :
   # q=s.attributes['field'].value
    q.append(s.attributes['field'].value)
    m.append(s.firstChild.nodeValue)
    print ("Attribute Name : ", s.attributes['field'].value)
    print ("Text : ", s.firstChild.nodeValue)

import pandas as pd    

x=pd.DataFrame(q)
y=pd.DataFrame(m)
data=pd.concat([x,y],axis=1,ignore_index=False)
#data1=data.T
#data1.columns = data1.iloc[0]
#data1=data1.reindex(data1.index.drop(0))


def dataframess(D):
    D=pd.DataFrame(D)
    D=D.T
    D.columns = D.iloc[0]
    D=D.reindex(D.index.drop(0))
    return D

   
def splitt(D):
    Size=61
    lists=[D.loc[i:i+Size-1,:] for i in range(0,len(data),Size)]
    return lists



list_of_Data=splitt(data)

#D4=data.iloc[:61,:].values
D4=list_of_Data[0].as_matrix()
D4=dataframess(D4)




#D3=data.iloc[61:122,:].values
D3=list_of_Data[1].as_matrix()
D3=dataframess(D3)



#D2=data.iloc[122:183,:].values
D2=list_of_Data[2].as_matrix()
D2=dataframess(D2)


#D1=data.iloc[183:244,:].values
D1=list_of_Data[3].as_matrix()
D1=dataframess(D1)


#D0=data.iloc[244:304,:].values
D0=list_of_Data[4].as_matrix()
D0=dataframess(D0)


D0,D1=D0.align(D1,axis=1,fill_value=0)
D2,D1=D2.align(D1,axis=1,fill_value=0)
D3,D1=D3.align(D1,axis=1,fill_value=0)
D4,D1=D4.align(D1,axis=1,fill_value=0)
    
D=[D4,D3,D2,D1,D0]
newtable=pd.concat(D)

cols=list(newtable)
cols.insert(0,cols.pop(cols.index('fiscalyear')))
newtable=newtable.ix[:,cols]
newtable.reset_index()

newtable.to_csv('example.csv',index=False)







        
    

            