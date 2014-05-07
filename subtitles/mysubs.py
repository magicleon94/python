import urllib,urllib2
import re

serie_test = "revolution"
season_test = int('01')     #trasforma '01' in '1' et similia
episode_test = "14"
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
    seasonlist[season_number]=match[1][0]
    season_number+=1
if not (season_test in seasonlist):
        raise "Stagione non trovata"




    

