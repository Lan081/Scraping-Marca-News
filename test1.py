#import time
from bs4 import BeautifulSoup
import urllib.request
import requests
import sqlite3

conn = sqlite3.connect('my_database.sqlite')
cursor = conn.cursor()


#url = "https://www.marca.com/futbol/barcelona.html?intcmp=MENUESCU&s_kw=barcelona"

TeamsList = ("atletico","barcelona","real-madrid","valencia","sevilla","espanyol",
"betis","alaves","athletic","eibar","celta","getafe","huesca","leganes",
"levante","rayo","valladolid","villarreal","real-sociedad","girona")

urlbase = "https://www.marca.com/futbol/%s.html" 
for CurrentTeam in TeamsList:
    url = urlbase % (CurrentTeam)
    print("Retrieving news from %s..." %(CurrentTeam))
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
   
    good_html = soup.prettify()
    results = soup.find_all('ul', attrs={"class":"auto-items"})
    try:
        headers = results[0].findAll('header',attrs={"class":"mod-header"})
        for i in headers:    
            hreflink = i.findAll('a')
            Title = hreflink[0]['title']
            Link = hreflink[0]['href']    
            Team = CurrentTeam
            StartDate = Link.find('2019')
            Date = (Link[StartDate:StartDate+10])
            params = (Team,Date,Link,Title)
            cursor.execute('SELECT * FROM News WHERE (Title=? AND Team=?)',(Title,CurrentTeam))
            entry = cursor.fetchone()
            if entry is None:
                cursor.execute("INSERT INTO News VALUES (NULL, ?, ?, ?, ?)", params)
                print("    New entry added")
    except IndexError:
        print("    Error trying to get news from %s..." %(CurrentTeam))          

conn.commit()
conn.close()