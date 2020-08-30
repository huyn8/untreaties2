import pandas as pd
import os
import csv

"""
DATA CREATION
"""
#Reading in content (data) of all the txt files
path = os.getcwd() + r'/phase 2/dataset'
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

########## KMEANS FUNCTION ##########
# @PRECONDITION: The following parameter inputs are valid 
# 1. n_clusters: The number of clusters to form as well as the number of centroids to generate.
#
# 2. ‘k-means++’ : Method for initialization:
#     - selects initial cluster centers for k-mean clustering in a smart way to speed up convergence. 
#
# 3. max_iter: Maximum number of iterations of the k-means algorithm for a single run.
#
# 4. n_init: Number of time the k-means algorithm will be run with different centroid seeds. 
#   The final results will be the best output of n_init consecutive runs in terms of inertia.


# #create vectorizer usingTfidfVectorizer class to fit and transform the document text
# vectorizer = TfidfVectorizer(stop_words='english')
# dfclean =  df_copy['cleanedContent'].values.tolist()
# #print(dfclean)  
# X = vectorizer.fit_transform(dfclean)
    
# true_k = 6
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
# model.fit(X)

# # get the centroids and features
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()

# # print the centroids into which clusters they belongs
# for i in range(true_k):
#     print('Cluster %d:' % i),
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind])

# # predict the text sentence 
# print('\n')
# print('Prediction')
# prediction = model.predict(X)
# print(prediction)

"""
MODELING
BRUTE FORCE
"""
# Create column name to write csv 
col_name = ['treatyNum', 'prec1','prec4','oblig1','oblig2','oblig3','oblig5','deleg1','deleg2','deleg3','Flexibility','Withdrawal']

# dataframe of treaty number and content to list 
content_list = df['cleanedContent'].values.tolist()
tn_list = df['treatyNum'].values.tolist()

# Make a list of keywords 
prec1_list = ['must','should','can','shall'] 
prec4_list = ['annex','index','appendix','schedules','schedule']
oblig1_list = ['dispute','arbitration','mediation']   # ADD MORE
oblig2_list = ['monitor','data','report','collection','submission','investigation']
oblig3_list = ['']   # CHECK WITH BREE
oblig5_list = ['domestic','national authorities','rights of action','legislation']
deleg1_list = ['International Labor Organization','International Court of Justice']   # ADD MORE
deleg2_list = ['court','commision','tribunal','task force']    # ADD MORE
deleg3_list = ['']   # CHECK WITH BREE
f_list = ['reservation']   # ADD MORE
w_list = ['denunciation, expiry, terminate, termination, withdrawal']   # ADD MORE

# numpy array for csv final output
row_content = np.empty((0, 12), str)
i = 0

# for each treaty...
for txt in content_list:

    treatyNumber = tn_list[i]
    i+=1
    # default as n
    prec1, prec4, oblig1,oblig2,oblig3,oblig5,deleg1,deleg2,deleg3,flexibility,withdrawal = ['n','n','n','n','n','n','n','n','n','n','n']

    for elem in prec1_list:
        if(elem in txt):
            prec1 = 'y'
            continue
        
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
    
    #########  WORK ON THIS   ##########
    # Inducements to compliance are attempts to change the payoffs for cooperation and defection.
    for elem in oblig3_list:
        if(elem in txt):
            oblig3_list ='y'
            continue
    
    # Does this agreement entrust third parties with monitoring?
    for elem in deleg3_list:
        if(elem in txt):
            deleg3 = 'y'
            continue

    row_content = np.append(row_content, np.array([[treatyNumber,prec1,prec4,oblig1,oblig2,oblig3,oblig5,deleg1,deleg2,deleg3,flexibility,withdrawal]]), axis=0)
    
with open('computerLabel.csv', 'w', newline='', encoding='utf8',) as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(col_name)
    writer.writerows(row_content)
    csv_file.close()
    
#IN PROGRESS...