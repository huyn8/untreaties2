import pandas as pd
import os
import csv

"""
DATA CREATION
"""
#Reading in content (data) of all the txt files
path = os.getcwd() + r'\dataset'
file_content = []
for file in os.listdir(path):
    try:
        f = open(path + '\\' + file, 'r', encoding='utf8')
        file_content.append([os.path.splitext(file)[0], f.read()])
    except Exception:
        print("Error")

#Putting the data above into a csv file
col_names = ['treatyNum', 'content']
with open('dataset.csv', 'w', newline='', encoding='utf8',) as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(col_names)
    for i in file_content:
        writer.writerow(i)
    csv_file.close()

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

# Panda dataframes (2d) can be broken down into series (1d)
# Cleaning a panda 1d array (series)
# Cleaning \r and \n, quotation marks, large spaces, possessive words
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
    df_copy['cleanedContent']  = df_copy['cleanedContent'] .str.replace(punctuation, '')

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
DATA ANALYSIS
"""
#TBD


"""
FEATURE ENGINEERING
"""
#IN PROGRESS...



"""
MODELING
"""
#IN PROGRESS...