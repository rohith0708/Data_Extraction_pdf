# import section
from django.shortcuts import render
from .forms import dataform
from PyPDF2 import PdfReader 
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
import cv2
import os
import re
import pandas as pd
import csv

# Creates views for handling the uploaded pdf and showing the exracted data
def index(request):

    ## saving files uploaded by user

    if request.method == 'POST':
     form=dataform(request.POST,request.FILES)
     if form.is_valid():
        instance=form.save()
        filename=instance.pdf.name
        pdffile=os.path.join('media/{}'.format(filename))

        ##Script for converting to csv format
        ##1 read te file

        if os.path.exists(pdffile):
            reader = PdfReader(pdffile) 
            page = reader.pages[0]     

            for i in page.images:
                with open(i.name,'wb') as d:
                    d.write(i.data)
                imgname=i.name
            img=cv2.imread('{}'.format(imgname))
            text=pytesseract.image_to_string(img)

            ##removed unwanted text like '=' when converting into csv
            remove='='
            newtext = re.sub(re.escape(remove),"",text)

            ##function for identifying start and end of table in invoice
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

            ## created table and stoting in dictionary
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

            ## converted dictionary into csv format using pandas
            df=pd.DataFrame(result)
            df.to_csv('result.csv',index=False)

            ## extracting headers
            for i in lines:
                if 'invoice' in i.lower():
                    invoice=i
                if 'payment date' in i.lower():
                    payment=i
        
            csv_file_path = 'result.csv'

            ## open csv file and and pass data to table as context
            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                data = list(csv_reader)

            context = {'data': data,'invoice':invoice,'payment':payment}
          
        return render(request,'result.html',context)
        
          


    else:
        form=dataform()
    
    ## webpage for uploading pdf and passed form as context
    return render(request, 'index.html',{'form':form})