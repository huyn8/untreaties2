import pandas as pd
import os
import csv
import math

"""
The purpose of this program is to label text data into different categories 
The different blocks of code below explain the processes of this program
There are additional in-line comments in each block of code for
further details on what a specfic part of the code does
The import statements in "CLEANING DATA" section have to be uncommented
for first time run to download necessary dependencies (packages). After that
they can be commented again to avoid repeated downloads 

"""

"""
SUPPORTING FUNTIONS (TO-DOs)
"""
#For converting from pdf to txt
def convert_pdf_to_txt(pdf):
    return 0

#For converting from word to txt
def convert_word_to_txt(word):
    return 0

#For counting words
def count_words(txt_file):
    word_count = 0
    return word_count



"""
DATA CREATION
"""
#Reading in content (data) of all the txt files
# path = os.getcwd() + r'/phase 2/dataset'
# file_content = []
# for file in os.listdir(path):
#     try:
#         f = open(path + '\\' + file, 'r', encoding='utf8')
#         file_content.append([os.path.splitext(file)[0], f.read()])
#     except Exception:
#         print("Error")

# #Putting the data above into a csv file
# col_names = ['treatyNum', 'content']
# with open('dataset.csv', 'w', newline='', encoding='utf8',) as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(col_names)
#     for i in file_content:
#         writer.writerow(i)
#     csv_file.close()

"""
CLEANING DATA
"""
#This part is here to resolve encoding problem in the print() statement (don't delete)
import sys
sys.stdout.reconfigure(encoding='utf-8')

#Loading the csv file data into panda dataframe
file_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
df = pd.read_csv(file_path)

#Uncomment to see the data in this dataframe 
# print (df.head(3))

#Importing appropriate libraries for data cleaning
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#uncomment these three lines for first execution of the code
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
import numpy as np

#Using the df_copy instead of the orginal dataframe
df_copy = df.copy(deep=True)

#Displaying the content the second treaty in the dataframe
#Uncomment to see the data before cleaning
# print('Before cleaning:')
# print(df_copy.head(3))
# print(df_copy.loc[1]['content'])

#Panda dataframes (2d) can be broken down into series (1d)
#Cleaning a panda 1d array (series)
#Cleaning \r and \n, quotation marks, large spaces, possessive words
df_copy['cleanedContent'] = df_copy['content'].str.replace("\r", " ")
df_copy['cleanedContent'] = df_copy['cleanedContent'].str.replace("\n", " ")
df_copy['cleanedContent'] = df_copy['cleanedContent'].str.replace("    ", " ")
df_copy['cleanedContent'] = df_copy['cleanedContent'].str.replace('"', '')
df_copy['cleanedContent'] = df_copy['cleanedContent'].str.replace("'s","")

#Changing all texts to lower case
df_copy['cleanedContent'] = df_copy['cleanedContent'].str.lower()

#Cleaning punctuation
punctuations = list("?:!.,;~﻿")

for punctuation in punctuations:
    df_copy['cleanedContent']  = df_copy['cleanedContent'].str.replace(punctuation, '')

#Initializing a lemmatizer object
wordnet_lemmatizer = WordNetLemmatizer()

#Lemmtizing
nrows = len(df_copy)
lemmatized_text_list = []

for row in range(0, nrows):
    # Create an empty list containing lemmatized words
    lemmatized_list = []

    # Save the text and its words into an object
    text = df_copy.loc[row]['cleanedContent']
    text_words = text.split(" ")

    # Iterate through every word to lemmatize
    for word in text_words:
        lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))

    # Join each word back together seperated by a space
    lemmatized_text = " ".join(lemmatized_list)
    
    # Append to the list containing the texts
    lemmatized_text_list.append(lemmatized_text)

df['cleanedContent'] = lemmatized_text_list

#Stop words removing
stop_words = list(stopwords.words('english'))

for stop_word in stop_words:
    regex_stopword = r"\b" + stop_word + r"\b"
    df_copy['cleanedContent'] = df_copy['cleanedContent'].str.replace(regex_stopword, '')

#Uncomment to see the data after cleaning
# print('After cleaning:')
# print(df_copy.head(3))
# print(df_copy.loc[1]['cleanedContent'])


"""
LABELING & CLASSIFYING
"""
# Create column name to write csv 
col_name = ['treatyNum', 'prec1','prec3','prec4','oblig1','oblig2','oblig3','oblig4','oblig5','deleg1','deleg2','deleg3','flexibility','withdrawal']

# dataframe of treaty number and content to list 
content_list = df['cleanedContent'].values.tolist()
tn_list = df['treatyNum'].values.tolist()

# Make a list of keywords 
prec1_list = ['must','should','can','shall'] 
prec4_list = ['annex','index','appendix','schedules','schedule','map','maps']
oblig1_list = ['dispute','arbitration','mediation','court','settlement','dispute settlement body', 'appellate body', 'investment court system']  
oblig2_list = ['monitor','data','report','collection','submission','investigation']
oblig3_list = ["curtail", "censure", "sanction", "expell", "expulsion"]  
oblig5_list = ['domestic','national authorities','rights of action','legislation']
deleg1_list = ['international labor organization','international court of justice',"nonprofit", "civil society", "observer", "non governmental organization", "ngo"]  
deleg2_list = ['commision','tribunal','task force']# These words are all good, but one key thing is they have to be paired with something that creates or modifies it. 
oblig4_hard = ['must', "will", "may not", "may", "shall"]
oblig4_soft = ["try", "endeavor", "put effort", "work toward", "encourage", "urge"]
deleg3_list = ['lodge complaint', 'monitor']  
f_list = ['reservation','opt out', "inequitable burden", "emergency circumstance", "escape"]
w_list = ['denunciation, expiry, terminate, termination, withdrawal'] 

# numpy array for csv final output
row_content = np.empty((0, 14), str)
i = 0

# for each treaty...
for txt in content_list:

    treatyNumber = tn_list[i]
    i+=1
    # default as n
    prec1, prec3, prec4, oblig1,oblig2,oblig3,oblig5,deleg1,deleg2,deleg3,flexibility,withdrawal = ['n',0,'n','n','n','n','n','n','n','n','n','n']

    # Count words in txt for prec3
    count = len(txt.split())
    prec3 = str(count)
    
    # Count the soft and hard words for oblig4
    count_soft = 0
    count_hard = 0
    for elem in oblig4_hard:
        if(elem in txt):
            count_hard += 1
    for elem in oblig4_soft:
        if(elem in txt):
            count_soft += 1

    # check the ratio between hard and soft law keywords
    if(count_soft == count_hard ):
        oblig4 = 3
    elif(count_soft == 0):
        oblig4 = 5
    elif(count_hard == 0):
        oblig4 = 1
    elif(count_soft < count_hard):
        oblig4 = 4
    elif(count_soft > count_hard):
        oblig4 = 2
    
    # prec1
    for elem in prec1_list:
        if(elem in txt):
            prec1 = 'y'
            continue
    
    # prec4
    for elems in prec4_list:
        if(elems in txt):
            prec4 = 'y'   
            continue 
    
    #Is there a dispute resolution provision?
    for elem in oblig1_list:
        if(elem in txt):
            oblig1 ='y'
            continue
    
    #Does the agreement call for compliance monitoring?
    for elem in oblig2_list:
        if(elem in txt):
            oblig2 ='y'
            continue
    
    # Is the agreement explicit about domestic legislation?
    for elem in oblig5_list:
        if(elem in txt):
            oblig5 = 'y'
            continue
    
    # Does the agreement confer any rights or responsibilities to non-state actors?
    for elem in deleg1_list:
        if(elem in txt):
            deleg1 = 'y'
    
    # Does the agreement create any new bodies?
    for elem in deleg2_list:
        if(elem in txt):
            deleg2 = 'y'
            continue
    
    # Is there a provision allowing reservations, an opt out clause, or an escape clause?
    for elem in f_list:
        if(elem in txt):
            flexibility = 'y'
            continue
    
    # Does the agreement include a withdrawal clause?
    for elem in w_list:
        if(elem in txt):
            withdrawal = 'y'
            continue
    
    # Inducements to compliance are attempts to change the payoffs for cooperation and defection.
    for elem in oblig3_list:
        if(elem in txt):
            oblig3 = 'y'
            continue
    
    # Does this agreement entrust third parties with monitoring?
    for elem in deleg3_list:
        if(elem in txt):
            if(deleg1 == 'y'):
                deleg3 = 'y'
                continue

    row_content = np.append(row_content, np.array([[treatyNumber,prec1,prec3,prec4,oblig1,oblig2,oblig3,oblig4,oblig5,deleg1,deleg2,deleg3,flexibility,withdrawal]]), axis=0)
    
with open('computerLabel.csv', 'w', newline='', encoding='utf8',) as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(col_name)
    writer.writerows(row_content)
    csv_file.close()
    
#IN PROGRESS...