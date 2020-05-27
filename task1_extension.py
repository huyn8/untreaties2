
import requests
import os
from bs4 import BeautifulSoup

base_url = "https://treaties.un.org"


"""
Function to open a URL
This function takes in a URL and turns it into a python readble object

params: url
pre: a valid url
post: a python object
returns: a python object

"""
def open_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


"""
Function to download a pdf
This function takes in a downloadble pdf link and a pdf name
to create a pdf

params: requires a pdf link
pre: a working pdf link 
post: a .pdf file
return: nothing

"""
def download_pdf(pdf_link):
    downloaded = False
    r = requests.get(pdf_link, stream = True)
    with open(pdf_link.split('/')[-1],"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024): 
            # writing one chunk at a time to pdf file 
            if chunk: 
                pdf.write(chunk) 
        pdf.close()
        downloaded = True
    #if not pdf was not sucessfully downloaded, redownload
    if not downloaded:
        download_pdf(pdf_link)


"""
Function to locate a downloadable pdf
This function is for locating a downloadable pdf link on the site

params: requires url of the pdf
pre: a valid url 
post: none
return: nothing

"""
def find_and_download_pdfs(url):
    tag_id = 'ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_rptText_ctl00_hypCTC'
    try:
        new_page = open_page(url)
        pdf_link = new_page.find(id = tag_id)
        download_pdf(base_url + pdf_link['href'])
    except:
        return


"""
Pages processing 
What this piece of code does:
1. Opens the given url and turns it into a processable python object
2. Looks for the approriate data for extraction (data in this case are pdf files)
3. Calls functions to locate and download approriate pdf files
4. Creates approriate folders to store corresponding downloaded pdfs 

"""
url = "https://treaties.un.org/Pages/ParticipationStatus.aspx?clang=_en"
original_page = open_page(url)
table_content_id = "ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgSubChapterList"
links = original_page.table.find_all('a')

for link in links:
    os.mkdir(link.get_text())
    os.chdir(os.getcwd()+'\\'+str(link.get_text()))

    new_page = open_page(base_url + "/Pages/"+ link['href'])
    table_links = new_page.find(id = table_content_id).find_all('a')
    for table_link in table_links:
        try:
            find_and_download_pdfs(base_url+ "/Pages/"+ table_link['href'])
        except:
            continue
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))


