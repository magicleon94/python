# -*- coding: utf-8 -*-
import urllib, urllib2
import cookielib
import re
import zipfile
import os,sys


def download_episode(epnumber, eplist):
    if not (epnumber in eplist):
        print "Episodio " + str(epnumber) + " non trovato"
        return
    if verbose==1:
        print "Episodio trovato. Procedo al download dell'episodio " + str(epnumber) + "."
    #apro la pagina del sottotitolo
    url = opener.open(eplist[epnumber])
    page = url.read()
    url.close()
    match = re.search('<!-- End of remositorypathway-->(.*?)<!-- End of remositoryfileinfo -->',page,re.DOTALL)
    match = re.findall(serie+'(.*?)</center></h2><dt><br /><center><a href="(.*?)" rel="nofollow">',match.group(1),re.DOTALL | re.IGNORECASE)
    if len(match)<1:
        print "Si è verificato un errore col download dell'episodio\nProbabilmente i dati di login sono errati."
        print "Ricontrolla i dati aprendo lo script con un qualunque editor di testo e modifica i valori delle variabili username e password"
        quit()
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

def highresolutions(res,page):
    match = re.search("<div id='remositorycontainerlist'>(.*?)<!-- End of remositorycontainerlist -->",page,re.DOTALL)
    match = re.findall('<a href="(.*?)"> (.*?)</a>',match.group(1),re.DOTALL)
    for x in match:
        if x[1]==res:
            return x[0]
    return ''
##############################################################################################################

if len(sys.argv)<=4:
    print "Execute with the following arguments:"
    print "serie_name season_number episode_number directory <options>"
    print "edit the username and password variables to log in correctly"
    quit()

serie = sys.argv[1]
season = int(sys.argv[2])
episode = int(sys.argv[3])
directory = sys.argv[4]
tmp_file = 'tmp.zip'
res = 'default'
verbose = 0
ranged = 0
for opt in sys.argv:
    if opt == '--verbose':
        verbose = 1
    elif opt == '--720p':		
        res = '720p'				
    elif opt == '--1080p':
        res = '1080p'
    elif opt == '--1080i':
        res = '1080i'
    elif opt == '--range':
        ranged = 1
if ranged == 1:
    inf = int(raw_input("Inserire l'estremo inferiore del range di episodi\n"))
    sup = int(raw_input("Inserire l'estremo superiore del range di episodi\n"))


#modificare solo questi dati
username = 'TUO_USERNAME'
password = 'TUA_PASSWORD'



#login
login_url = 'http://www.italiansubs.net/index.php'
login_data = {'username':username,'passwd':password,'remember':'yes', 'option':'com_user','task':'login','silent':'true','return':'aHR0cDovL3d3dy5pdGFsaWFuc3Vicy5uZXQv','4e48ce6d96cc53787c1154ca49da26b8':'1'}
datas = urllib.urlencode(login_data)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
page = opener.open(login_url,datas)
page.close()
if verbose==1:
    print "Login effettuato"
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
if verbose==1:
    print "Serie  '", serie , "' trovata!"
#apro link serie
url = opener.open(serieslist[serie])
page = url.read()
url.close()
del(serieslist)  #non mi serve più, la dealloco

#ricerca stagione
match = re.search('</tr></thead><tbody>(.*?)</tbody>',page,re.DOTALL)
match = re.findall('<a href="(.*?)> Stagione (.*?)</a>',match.group(1),re.DOTALL)
seasonlist = {}
for x in match:
    seasonlist[int(x[1])] = x[0]
if not (season in seasonlist):
    raise "Stagione non trovata"
if verbose==1:
    print "Stagione " + str(season) + " trovata!"

#apro link stagione
url = opener.open(seasonlist[season])
page = url.read()
url.close()
del(seasonlist) #non mi serve più, la dealloco

#costruisco lista episodi
if res!='default':
    print "risoluzione diversa"
    new_url = highresolutions(res,page)
    if new_url!='':
        if verbose==1:
            print "Risoluzione ", res, " trovata!"
        url = opener.open(new_url)
        page = url.read()
        url.close
    else:
        if verbose==1:
            print "Risoluzione non trovata, procedo al download standard"
        
match = re.search("<div id='remositoryfilelisting'>(.*?)<!-- End of remositoryfilelisting -->",page,re.DOTALL)
match = re.findall(';<a href="(.*?)">'+ str(serie) + ' ' + str(season) + 'x'+'(.*?)</a>',match.group(1),re.DOTALL | re.IGNORECASE)
episodelist = {}
for x in match:
    if len(x[1])==2:
        episodelist[int(x[1])]=x[0]
if ranged == 0:
    download_episode(episode,episodelist)
else:
    for i in range(inf,sup+1):
        download_episode(i,episodelist)
  
print 'ok'


