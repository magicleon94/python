import urllib, urllib2
import cookielib
import re
import zipfile
import os,sys

#stesura grezza, molto grezza
"""
if len(sys.argv)<=1:
    print "Execute with the following arguments:"
    print "serie_name season_number episode_number directory"
    print "edit the username and password variables to log in correctly"
    quit()

serie = sys.argv[1]
season = int(sys.argv[2])
episode = int(sys.argv[3])
directory = sys.argv[4]
tmp_file = 'tmp.zip'

"""
serie = "game of thrones"
season = int('4') 
episode = int("6")
episode_range = (1,14)
tmp_file= 'tmp.zip'
directory = './'

username = 'username_here'
password = 'password_here'
#login
login_url = 'http://www.italiansubs.net/index.php'
login_data = {'username':username,'passwd':password,'remember':'yes', 'option':'com_user','task':'login','silent':'true','return':'aHR0cDovL3d3dy5pdGFsaWFuc3Vicy5uZXQv','4e48ce6d96cc53787c1154ca49da26b8':'1'}
datas = urllib.urlencode(login_data)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
page = opener.open(login_url,datas)
page.close()
#loggato

url = urllib.urlopen('http://www.italiansubs.net/index.php?option=com_remository&Itemid=9#482')
page = url.read()
url.close()
#ricerca della serie
match = re.search('</tr></thead><tbody>(.*?)</body>',page,re.DOTALL)
match = re.findall('<a href="(.*?)"> (.*?)</a>',match.group(1),re.DOTALL)
serieslist = {}
for x in match:
    serieslist[x[1].lower()] = x[0]

if not (serie in serieslist):
    raise "Serie non trovata"
url = opener.open(serieslist[serie])
page = url.read()
url.close()

#ricerca stagione
match = re.search('</tr></thead><tbody>(.*?)</tbody>',page,re.DOTALL)
match = re.findall('<a href="(.*?)> Stagione (.*?)</a>',match.group(1),re.DOTALL)
seasonlist = {}
for x in match:
    seasonlist[int(x[1])] = x[0]
if not (season in seasonlist):
    raise "Stagione non trovata"

#ricerco episodi
url = opener.open(seasonlist[season])
page = url.read()
url.close()
match = re.search("<div id='remositoryfilelisting'>(.*?)<!-- End of remositoryfilelisting -->",page,re.DOTALL)
match = re.findall(';<a href="(.*?)">'+ str(serie) + ' ' + str(season) + 'x'+'(.*?)</a>',match.group(1),re.DOTALL | re.IGNORECASE)
episodelist = {}
for x in match:
    if len(x[1])==2:
        episodelist[int(x[1])]=x[0]
if not (episode in episodelist):
    raise ("Episodio non trovato")
#apro la pagina del sottotitolo
url = opener.open(episodelist[episode])
page = url.read()
url.close()

match = re.search('<!-- End of remositorypathway-->(.*?)<!-- End of remositoryfileinfo -->',page,re.DOTALL)
match = re.findall(serie+'(.*?)</center></h2><dt><br /><center><a href="(.*?)" rel="nofollow">',match.group(1),re.DOTALL | re.IGNORECASE)

download_url = match[0][1]
download_page = opener.open(download_url)
zippy = download_page.read()
download_page.close()
zipped_sub = open(tmp_file,'wb')
zipped_sub.write(zippy)
zipped_sub.close()

zipped_sub = open(tmp_file)
zipobj = zipfile.ZipFile(zipped_sub)
zipobj.extractall(directory)
zipobj.close()
zipped_sub.close()
os.remove(tmp_file)
  

print 'ok'


