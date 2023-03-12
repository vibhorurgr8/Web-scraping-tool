import requests
from bs4 import BeautifulSoup
import sqlite3
# url of the website you need to scrape
url = 'https://www.imdb.com/search/title/?title_type=feature&count=250'#base url
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
urls = [url]#contains all the urls to be scraped
ls = []
#function to make soup from url
def makeSoup(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

#function to flip pages and generate its urls
def pageLoop(url):
    for i in range(3):
        next = makeSoup(url).find(class_="lister-page-next next-page").get('href')
        url = ('https://www.imdb.com'+str(next))
        urls.append(url)
pageLoop(url)
print(urls)

def extracter(urls):
    index = 1
    for i in urls:
        items = makeSoup(i).find_all('div', class_="lister-item mode-advanced")
        
        for item in items:
            name = item.find(class_="lister-item-content").h3.a.text.strip()
            # print(name)
            year = item.find(class_="lister-item-year").text
            # print(year)
            genre = item.find(class_="genre").text.strip()
            # print(genre)
            try:
                runtime = item.find(class_="runtime").text.strip()
            except:
                runtime = None
            # print(runtime)
            try:
                rating = item.find(class_="inline-block ratings-imdb-rating").text.strip()
            except:
                rating = None
            # print(rating)
            ls.append((index, name, year, genre, runtime, rating))
            index+=1
extracter(urls)
print(ls)
