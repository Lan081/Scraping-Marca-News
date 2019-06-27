import time
from bs4 import BeautifulSoup
import urllib.request
import requests
import sqlite3

conn = sqlite3.connect('my_database.sqlite')
cursor = conn.cursor()


#url = "https://www.marca.com/futbol/barcelona.html?intcmp=MENUESCU&s_kw=barcelona"

TeamsList = ("atletico","barcelona","real-madrid","valencia","sevilla","espanyol","betis","alaves")

urlbase = "https://www.marca.com/futbol/%s.html" 
newurl = (urlbase,"atletico")
for CurrentTeam in TeamsList:
    url = urlbase % (CurrentTeam)
    print("Retrieving news from %s..." %(CurrentTeam))
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    good_html = soup.prettify()
    results = soup.find_all('ul', attrs={"class":"auto-items"})
    #f = open("noticias.txt","w+") //In case save in file
    headers = results[0].findAll('header',attrs={"class":"mod-header"})
    for i in headers:    
         hreflink = i.findAll('a')
         Title = hreflink[0]['title']
         Link = hreflink[0]['href']    
         Team = CurrentTeam
         Date = " "
        #f.write("Titulo: " + title + "Enlace: " + link) //In case save in file
        # #date
         params = (Team,Date,Link,Title)
         cursor.execute("INSERT INTO News VALUES (NULL, ?, ?, ?, ?)", params)


#f.close() //In case save in file
conn.commit()
conn.close()