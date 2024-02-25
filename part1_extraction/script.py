# 1 import section
from PyPDF2 import PdfReader 
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
import cv2
import re
import csv
import pandas as pd

# 2 reading pdf and converting into image section
reader = PdfReader('sample1.pdf') 
page = reader.pages[0] 
file='data/'
for i in page.images:
    with open(i.name,'wb') as f:
   
     f.write(i.data)

    imgname=i.name


#3 reading text from image 
img=cv2.imread('{}'.format(imgname))
text=pytesseract.image_to_string(img)

#4 removed unwanted text like '=' when converting into csv
remove='='
newtext = re.sub(re.escape(remove),"",text)


#5 function for identifying start and end positions of table
def start_end(datalist):
   start,end=[],[]
   for ind,line in enumerate(datalist):
      if 'reference' in line.lower():
        start.append(ind)
      if 'length' in line.lower():
         end.append(ind)
   return start,end

lines=[]
for line in newtext.splitlines():
    lines.append(line.strip())
start,end=start_end(lines)   
istart=int(''.join(map(str,start)))
iend=int(''.join(map(str,end)))

#6 extracting headers
for i in lines:
   if 'invoice' in i.lower():
      print(i)
   if 'payment date' in i.lower():
      print(i)  


#7 extracting table and storing in result dictionary
result={
   
   'Reference':[],
   'Designation':[],
   'Qty':[],
    'Unit_price':[],
    'Total_CHF':[],
    'sales':[],
    
}

for  i in lines[istart:iend]:   
   if 'work' not in i.lower() and 'and' not in i.lower() and 'exterior' not in i.lower() and 'reference' not in i.lower() :
      result['Reference'].append(i.split()[0])
      result['sales'].append(i.split()[-1])
      result['Total_CHF'].append(i.split()[-2])
      result['Unit_price'].append(i.split()[-3])
      result['Qty'].append(i.split()[-2])
      result['Designation'].append(' '.join( i.split()[2:-4]))

#8 converting into csv
df=pd.DataFrame(result)
df.to_csv('result.csv',index=False)
