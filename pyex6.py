#pyex6.py - Use BeautifulSoup parser to parse MU news archives
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

import requests
import bs4

url = requests.get('https://www.monmouth.edu/news/archives')

html = url.text

munews_soup = bs4.BeautifulSoup(html, 'html.parser')
#print(type(munews_soup))

articles = munews_soup.find_all('h2')

#print(articles[0])

titles = []
links = []
for article in articles:
    anchor = article.find('a')

    titles.append(anchor.text)
    links.append(anchor['href'])


newsfeed = {}
for title_num in range(len(titles)):
    newsfeed[titles[title_num]] = links[title_num]

print(newsfeed) 