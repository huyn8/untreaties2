import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl.workbook import Workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
SETTING UP
"""
url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
# type(soup)
# title = soup.title
# print(title)

# text = soup.get_text()
#print(soup.text)

# all_links = soup.find_all('a')
# for link in all_links:
#     print(link.get("href"))

rows = soup.find_all('tr')
# print(rows[:10])

for row in rows:
    row_td = row.find_all('td')
# print(row_td)
# type(row_td)
 
#cleaner way to do without using regular (re) expression
# str_cells = str(row_td)
# cleantext = BeautifulSoup(str_cells, "lxml").get_text()
# print(cleantext) 

#not so clean way to do using regular expression
import re

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
# print(clean2)
# type(clean2)

df = pd.DataFrame(list_rows)
df.head(10)

"""
DATA MANIPULATION AND CLEANING
"""
df1 = df[0].str.split(',', expand=True)

df1[0] = df1[0].str.strip('[')

col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
#print(all_header)

df2 = pd.DataFrame(all_header)

df3 = df2[0].str.split(',', expand=True)

#dataframes concatenation 
frames = [df3, df1]
df4 = pd.concat(frames)

df5 = df4.rename(columns=df4.iloc[0])

# df5.info()
# df5.shape

df6 = df5.dropna(axis=0, how='any')

df7 = df6.drop(df6.index[0])

df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)

df7['Team'] = df7['Team'].str.strip(']')

time_list = df7[' Chip Time'].tolist()

# You can use a for loop to convert 'Chip Time' to minutes

time_mins = []
for i in time_list:
    if len(i.split(':')) == 3:
        h, m, s = i.split(':')
        math = (int(h) * 3600 + int(m) * 60 + int(s))/60
        time_mins.append(math)
    else:
        m, s = i.split(':')
        math = (0 * 3600 + int(m) * 60 + int(s))/60
        time_mins.append(math)
        
# print(time_mins)

df7['Runner_mins'] = time_mins

# print(df7.describe(include=[np.number]))

from pylab import rcParams
rcParams['figure.figsize'] = 15, 5

#boxplot
# df7.boxplot(column='Runner_mins')
# plt.grid(True, axis='y')
# plt.ylabel('Chip Time')
# plt.xticks([1], ['Runners'])
#plt.show()

#barplot
# x = df7['Runner_mins']
# ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
# plt.show()

f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']==' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
# plt.legend()
# plt.show()

g_stats = df7.groupby(" Gender", as_index=True).describe()
# print(g_stats)

df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")
# plt.show()

df7.to_excel("completeoutput.xlsx")#for debugging purposes