# Reference: https://stackabuse.com/text-classification-with-python-and-scikit-learn/ ignoring text classification section 
#1: Importing libraries
import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
import pandas as pd


# Clean missing values + "special" values from the imported csv file
missingvals = ['NA','OAUcharter','LoN', 'EEC', 'ILO', '"Amazon Cooperation"','Multilateral Agreement for the Establishment of an International Think Tank for Landlocked Developing Countries','55 (a)', '20 (a)', '20 (b)','?']

# Change column name as needed 
col_names = ['prec4','prec1']

csv_data = pd.read_csv (r'/Users/kraynguyen1/Desktop/MLtreaty/FinalTreatyCombo.csv',na_values = missingvals) 

# fill na values with 0
csv_data.fillna(0)      

# make a subset of necessary variables
df = pd.DataFrame(csv_data,columns=col_names)

# Testing dataframe
print('dataframe:')
print(df.head())

# capitalize y and n, replace with 1 for yes, 0 for no. Input for training model only accepts float data type
df['prec1'] = df['prec1'].str.capitalize()
df['prec1'] = df['prec1'].replace(['Y','N','y','n'],['1','0','1','0'])

df['prec4'] = df['prec4'].str.capitalize()
df['prec4'] = df['prec4'].replace(['Y','N','N?','y','n','4'],['1','0','0','1','0','0'])

# cleaning 
#df['treatyNum'] = df['treatyNum'].replace(['266-I-3822','I-54669'],['3822','54669'])
df = df.dropna()

# x is prec 1 (dependent variable), y is prec 4 (predicting variable)
# Adjustable
X = df.drop('prec4',axis = 1).copy()
y = df.prec4.copy()

# splits into train and test. training 50% testing 50%
# Adjustable 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

############ train logistic regression model ########
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression() 
classifier.fit(X_train, y_train)
print('logistic regression report:')

######### train random forest model  ##########
from sklearn.ensemble import RandomForestClassifier
#classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
#classifier.fit(X_train, y_train) 

######### train linear SVC model ########
from sklearn.svm import SVC
#classifier = SVC(kernel = 'linear')
#classifier.fit(X_train,y_train)

##### Scaling for K-nearest neighbor model ######
from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#scaler.fit(X_train)
#X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)

######## Train K neighbor model  ########
from sklearn.neighbors import KNeighborsClassifier
#classifier = KNeighborsClassifier(n_neighbors=5)
#classifier.fit(X_train, y_train)

####### Train decision trees model ######
from sklearn.tree import DecisionTreeClassifier
#classifier = DecisionTreeClassifier()
#classifier.fit(X_train,y_train)

# prediction
y_pred = classifier.predict(X_test)

# Evaluating the model
from sklearn.metrics import classification_report, f1_score, accuracy_score
#print(f1_score(y_test, y_pred, average='weighted', labels=np.unique(y_pred)))
print(classification_report(y_test,y_pred))

print('Final Accuracy: ')
print(accuracy_score(y_test, y_pred))

#Save the model
with open('text_classifier', 'wb') as picklefile:
    pickle.dump(classifier,picklefile)

# Load the model
#with open('text_classifier', 'rb') as training_model:
    #classifier = pickle.load(training_model)

# classifier.predict(...)

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


# create vectorizer usingTfidfVectorizer class to fit and transform the document text
# vectorizer = TfidfVectorizer(stop_words='english')
# df =  df_copy['cleanedContent'].values.tolist()
# #print(df)
# X = vectorizer.fit_transform(df)

# true_k = 6
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
# model.fit(X)

# # get the centroids and features
# order_centroids = model.clustercenters.argsort()[:, ::-1]
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