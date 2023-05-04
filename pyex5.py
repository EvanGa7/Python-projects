# pyex5.py- html parsing with re
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

import re
import requests

url = "https://www.monmouth.edu/news/archives"

html = requests.get(url)
#print(type(html))
html_src = html.text
#print(html_src)

title_pattern = re.compile('target="_self" >(.+?)</a></h2>')

titles = title_pattern.findall(html_src)

print(titles)

links_pattern = re.compile('<a href="(.+?)" target="_self">')

links = title_pattern.findall(html_src)

print(links)

linkes = links_pattern.findall(html_src, re.DOTALL)

#print(len(links))

newsfeed = {}
for title_num in range(len(titles)):
    newsfeed[titles[title_num]] = links[title_num]

print(newsfeed)
