import requests
from bs4 import BeautifulSoup

"""
EXTRACTING AND FILTERING DATA
"""
url = "https://treaties.un.org/Pages/SearchResults.aspx?flag=Treaty&tab=UNTS"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

table = soup.body

print(type(table))

"""
PUTTING FILTERED DATA INTO EXCEL
"""