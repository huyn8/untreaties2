# import pandas as pd
# import numpy as np
import requests
import PyPDF2
import os
from bs4 import BeautifulSoup

"""
The purpose of this code is to access the provide URL and getting its content. 
The content in this case is a table with PDF files.
It then downloads the PDF files from the URL to the local machine.
The PDF files will then be converted to plain text files and sorted
into folders by year.

"""


'''
Getting the URL and converting it into a Python readable object

pre: A working URL with parsable data
post: a Python HTML object 
'''
url = "https://treaties.un.org/Pages/MSDatabase.aspx?clang=_en"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')


'''
The data of interest is only the table and nothing else on the website.
Extracting the table and its data.
After some cleaning up, the data is available to be used for the next step 
'''
table = soup.table 
links =  table.find_all('a') 
rows = table.find_all('tr')
years = []
for row in rows[1:]:
    years.append(row.td.get_text())#this whole thing could be refactored later

    
"""
Converting from PDF to plain text
Formating isn't 100% accurate, some non-character symbols might be missing 
but it should not affect the core content of the output file

pre: a PDF file
post: a .txt file
"""
def convert_to_txt(pdf_file):
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        txt_file = os.path.splitext(pdf_file)[0] +'.txt'
        with open (txt_file,'w', encoding="utf-8") as pdf_output:
            for page in range(pdf_reader.getNumPages()):
                data = pdf_reader.getPage(page).extractText()
                pdf_output.write(data)
        with open(txt_file, 'r') as pdf_content:
            pdf_content.read().replace('\n', ' ')
    

"""
After the data of interest have been indentified from the site, 
the data now contain PDF downloadable links.
This code does the following:
Downloading the PDF files from the site
Converting the PDF files into .txt files by calling the corresponding function 
Creating folders and sorting the PDF files and .txt files into 
appropriate folders by year 

pre: cleaned up data for PDF files download
post: PDF, .txt files and folders that are sorted by year

"""
link_num = 0
for year in years:
    month = 1
    os.mkdir(year)
    os.chdir(os.getcwd()+'\\'+str(year))
    while link_num < len(links):
        if year not in str(links[link_num]['href']):
            break
        else:
            r = requests.get(links[link_num]['href'], stream = True) 
            
            pdf_file_name = str(year)+"-"+str(month)+".pdf"
            
            with open(pdf_file_name,"wb") as pdf: 
                for chunk in r.iter_content(chunk_size=1024): 
                    # writing one chunk at a time to pdf file 
                    if chunk: 
                        pdf.write(chunk) 
            try:
                convert_to_txt(pdf_file_name)
                # os.remove(pdf_file_name)#is this step nessesary?
            except:
                print("")
            finally:
                month+=1
                link_num+=1
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

        # if link_num == 2:#delete later
        #     break#delete later

    
