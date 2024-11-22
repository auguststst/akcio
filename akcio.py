import re
import requests
import urllib
from bs4 import BeautifulSoup
from googlesearch import search
from youtubesearchpython import VideosSearch


class Spider:
    

    def __init__(self,q):
        self.q = q

    def get_ivi_soup(self):
        result = search(self.q + "смотреть онлайн www.ivi.ru")
        res = []
            
        for r in result:
            if "https://www.ivi.ru/watch" in r:
                res.append(r)

        p = res[0]
        page = requests.get(p)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def get_title(self):
        #re.findall("[^(]+(?= )", title)
        page = self.get_wikipedia_page()
        if page:
            page = requests.get(page)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup.findAll('th',{'class':'infobox-above'})[0].text
        else:
            soup = self.get_ivi_soup()
            title = soup.select('.breadCrumbs__item span')
            return(title[-1].text)

    def get_desc(self):
        soup = self.get_ivi_soup()
        return soup.select(".clause__text-inner p")[0].text

    def get_year(self):
        soup = self.get_ivi_soup()
        return soup.findAll('a',{'class':'parameters__link'})[0].text

    def get_country(self):
        soup = self.get_ivi_soup()
        return soup.findAll('a',{'class':'parameters__link'})[1].text


    def get_genres(self):
        soup = self.get_ivi_soup()
        genres = []
        genres.append(soup.findAll('a',{'class':'parameters__link'})[-1].text)
        genres.append(soup.findAll('a',{'class':'parameters__link'})[-2].text)
        genres.append(soup.findAll('a',{'class':'parameters__link'})[-3].text)
        return genres

    def get_telegram(self):
        return "https://t.me/joinchat/mZIPjtIHxjlhYzVi"

    def get_youtube(self):
        video = VideosSearch(self.q + "трейлер", limit = 2)
        result = video.result()
        link = result['result'][0]['link']
        l = re.findall("(?<=\/watch\?v=).*", link)
        return f"https://www.youtube.com/embed/{l[0]}"


    def get_wikipedia_page(self):
        result = search(self.q + "фильм википедия")
        r = []
        for x in result:
            if "ru" in x:
                r.append(x)

        r = urllib.parse.unquote(r[0])
        return r

    def get_imdb_link(self):
        page = self.get_wikipedia_page()
        page = requests.get(page)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.findAll('a',{'class':'extiw'})
        for x in result:
            if "https://www.imdb.com/title/" in x.get('href'):
                return x.get('href')
         
    
    def get_imdb(self):
        link = self.get_imdb_link()
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.findAll('span',{'class':'iTLWoV'})[0].text


web = Spider("код на миллиард долларов")
try:
    #print(web.get_image())
    
    print(web.get_title())
    print(web.get_desc())
    print(web.get_year())
    print(web.get_country())
    print(web.get_genres())
    #print(web.get_telegram())
    print(web.get_youtube())
    print(web.get_wikipedia_page())
    print(web.get_imdb()) 
except:
    print("error")