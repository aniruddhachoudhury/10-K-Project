# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 22:58:44 2019

@author: Aniruddha choudhury
"""

import re
import sys
#import urllib.request as ur

# = ur.urlopen("https://www.sec.gov/Archives/edgar/data/789019/000119312516662209/d187868d10k.htm")
#Data = url.read()

#new = open('edgar.txt', 'wb')
#new.write(Data)
#new.close()

#"https://www.sec.gov/Archives/edgar/data/789019/000119312516662209/d187868d10k.htm
#The above file url text is copied to a file.

recording = False
Data_file = "edgar.txt"
start_pattern = "^ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS"
stop_pattern = "^ITEM 8."
output_Data = []

for line in open(Data_file).readlines():
    if recording is False:
        if re.search(start_pattern, line) is not None:
            recording = True
            output_Data.append(line.strip())
    elif recording is True:
        if re.search(stop_pattern, line) is not None:
            recording = False
            sys.exit()
        output_Data.append(line.strip())
        
#To remove certaain strings from output data        
def remove(text):
        for word in output_Data[:]:
            if word.startswith(text):
                output_Data.remove(word)
        return output_Data    
NewData = remove('Table of Contents')
NewData1=remove('Item 8')


print ('\n'.join(output_Data))

#Save the extracted text in the output text file
extractedtext='\n'.join(output_Data)
textfile = open('textfile.txt', 'w')
textfile.write(extractedtext)
textfile.close()

#summarize of the item 7
from gensim.summarization import summarize
print (summarize(extractedtext))
summary=summarize(extractedtext)

#Save the extracted summary text in the output text file
textfile = open('summary.txt', 'w')
textfile.write(summary)
textfile.close()


