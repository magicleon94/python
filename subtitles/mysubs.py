import urllib, urllib2
import cookielib
import re
#stesura grezza, molto grezza
serie_test = "revolution"
season_test = int('02')     #trasforma '01' in '1' et similia
episode_test = int("20")
episode_range = (1,14)

url = urllib.urlopen('http://www.italiansubs.net/index.php?option=com_remository&Itemid=9#482')
page = url.read()
url.close()
#ricerca della serie
match = re.search('</tr></thead><tbody>(.*?)</body>',page,re.DOTALL)
match = re.findall('<a href="(.*?)"> (.*?)</a>',match.group(1),re.DOTALL)
serieslist = {}
for serie in match:
    serieslist[serie[1].lower()] = serie[0]

if not (serie_test in serieslist):
    raise "Serie non trovata"
url = urllib.urlopen(serieslist[serie_test])
page = url.read()
url.close()
#ricerca stagione
match = re.search('</tr></thead><tbody>(.*?)</tbody>',page,re.DOTALL)
match = re.findall('<a href="(.*?)> (.*?)</a>',match.group(1),re.DOTALL)
seasonlist = {}
season_number = 1
for season in match:
    seasonlist[season_number]=match[season_number-1][0]
    season_number+=1
if not (season_test in seasonlist):
        raise "Stagione non trovata"

#ricerco episodi
url = urllib.urlopen(seasonlist[season_test])
page = url.read()
url.close()

match = re.search("<div id='remositoryfilelisting'>(.*?)<!-- End of remositoryfilelisting -->",page,re.DOTALL)
match = re.findall(';<a href="(.*?)">'+ str(serie_test) + ' ' + str(season_test) + 'x'+'(.*?)</a>',match.group(1),re.DOTALL | re.IGNORECASE)

episodelist = {}
episode_number = 1
for ep in match:
    episodelist[episode_number]=match[episode_number-1][0]
    episode_number+=1
if not (episode_test in episodelist):
    raise "Episodio non trovato"

url = urllib.urlopen(episodelist[episode_test])
page = url.read()
url.close()

#match = re.search('<h2><br /><center>'+str(serie_test)+' '+str(season_test)+'x'+'(.*?) </center></h2><dt><br /><center><a href="(.*?)"',page,re.DOTALL)

urllib.urlretrieve('http://www.italiansubs.net/index.php?option=com_remository&Itemid=6&func=download&id=50580&chk=db89b463945dd4c3c5ad94f3eefd9af4&no_html=1','prova')

    

