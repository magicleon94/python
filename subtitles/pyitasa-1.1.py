#!/usr/bin/python
import re, urllib2, zipfile, os, sys
import urllib, urllib2, cookielib

# MEMO
# Calling the script works this way:
username = 'magicleonkennedy'
password = '957842658'

# Do not touch
loggedIn = 0
quiet = 0
resolution = '480p'
notFoundFiles = []
listSeries = {}
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

if (len(sys.argv)<=1):
  print 'Usage: ' + sys.argv[0] + ' [--quiet] [--720p] [--1080i] [--1080p] <file path 1> [<file path 2> ...]'
  quit()

if (len(sys.argv)>2):
  for line in sys.argv[2:]:
    if (line == '--quiet'):
      quiet = 1
    elif (line == '--720p'):
      resolution = '720p'
    elif (line == '--1080i'):
      resolution = '1080i'
    elif (line == '--1080p'):
      resolution = '1080p'
  
def findSubtitle(filePath):
  global loggedIn, listSeries

  filePathName = filePath.split('/')
  fileName = filePathName[len(filePathName)-1]

  match = re.search('(.*)\..*', filePath)
  fileWOExt = match.group(1)
  if (os.path.exists(fileWOExt + '.srt')):
    if (quiet == 0):
      print 'Subtitle for ' + fileName + ' already exists.'
    return 1
  
  match = re.search('(.*?) - (?:0)?([0-9]*)x([0-9]*) ', fileName)
  serieName = match.group(1)
  seasonNumber = match.group(2)
  episodeNumber = match.group(3)

  try:
    if (listSeries[serieName.lower()]['link'] != None):
      pass
  except KeyError:
    if (quiet == 0):
      print 'Gathering login data and looking for ' + serieName
    url = 'http://www.italiansubs.net/index.php?option=com_remository'
    usock = urllib2.urlopen(url)
    data = usock.read()
    usock.close()
    # Look for Series
    match = re.search('</tr></thead><tbody>(.*?)</tbody>', data, re.DOTALL)
    match = re.findall('<a href="(.*?)"> (.*?)</a>', match.group(1), re.DOTALL)
    for singleMatch in match:
      listSeries[singleMatch[1].lower()] = {}
      listSeries[singleMatch[1].lower()]['link'] = singleMatch[0]

    # Login!
    if (loggedIn == 0):
      # Gathering Login Data
      matchLogin = re.search('name=.return.*?value="(.*?)".*?name="(.*?)" value="1"', data, re.DOTALL)
      returnVal = matchLogin.group(1)
      sessionVal = matchLogin.group(2)
      if (quiet == 0):
        print 'return: ' + returnVal
        print 'session: ' + sessionVal
        print 'Logging in...'
      login_data = urllib.urlencode({'username': username, 'passwd': password, 'remember': 'yes', 'Submit': 'Login', 'option': 'com_user', 'task': 'Login', 'silent': 'true', 'return': returnVal, sessionVal: '1'})
      opener.open('http://www.italiansubs.net/index.php', login_data)
      loggedIn = 1

  try:
    if (listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber] != None):
      pass
  except KeyError:
    # Select tv serie and look for Seasons
    try:
      url = listSeries[serieName.lower()]['link']
    except KeyError:
      if (quiet == 0):
        print serieName + ' tv serie not found!'
      return 0
    if (quiet == 0):
      print serieName + ' tv serie found... looking for seasons...'
    usock = opener.open(url)
    data = usock.read()
    usock.close()
    match = re.search('</tr></thead><tbody>(.*?)</tbody>', data, re.DOTALL)
    match = re.findall('<a href="(.*?)"> (.*?)</a>', match.group(1), re.DOTALL)
    listSeries[serieName.lower()]['seasons'] = {}
    for singleMatch in match:
      listSeries[serieName.lower()]['seasons'][singleMatch[1].lower()] = {}
      listSeries[serieName.lower()]['seasons'][singleMatch[1].lower()]['link'] = singleMatch[0]

  # Select season and look for episodes
  try:
    if (listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['episodes'][seasonNumber + 'x' + episodeNumber] != None):
      pass
  except KeyError:
    try:
      url = listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['link']
    except KeyError:
      if (quiet == 0):
        print 'Season number ' + seasonNumber + ' not found!'
      return 0
    if (quiet == 0):
      print 'Season ' + seasonNumber + ' found. Looking for episodes...'
    usock = opener.open(url)
    data = usock.read()
    usock.close()
    
    if (resolution != '480p'):
      match = re.findall('<tr id="' + resolution + '">.*?<a href=\"(.*?)\">', data, re.DOTALL)
      if (len(match)==0):
        if (quiet == 0):
          print 'Resolution not found!'
        return 0
      listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['link'] = match[0]
      print 'Higher resolution found. Looking for episodes...'
      url = match[0]
      usock = opener.open(url)
      data = usock.read()
      usock.close()
    
    match = re.findall("<div class='remolist'>.*? src.*?fileinfo.*?>(.*?)</a>.*?'remolist3'.*?href='(.*?)'", data, re.DOTALL)
    listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['episodes'] = {}
    for singleMatch in match:
      episodeMatch = re.search(' ([0-9]+x[0-9]+)(?: )?$', singleMatch[0])
      try:
        listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['episodes'][episodeMatch.group(1)] = singleMatch[1]
      except AttributeError:
        pass

  # Select episode, download it, unzip it, move it to the the movies library and delete the zipfile.
  try:
    url = listSeries[serieName.lower()]['seasons']['stagione ' + seasonNumber]['episodes'][seasonNumber + 'x' + episodeNumber]
  except KeyError:
    if (quiet == 0):
      print 'Episode ' + seasonNumber + 'x' + episodeNumber + ' not found!'
    return 0
  usock = opener.open(url)
  data = usock.read()
  usock.close()
  file = open(fileWOExt + '.srt.zip',"wb")
  file.write(data)
  file.close()

  zfobj = zipfile.ZipFile(fileWOExt + '.srt.zip')
  if (quiet == 0):
    print 'Extracting ' + zfobj.namelist()[0] + ' into ' + fileWOExt + '.srt'
  file = open(fileWOExt + '.srt', 'wb')
  file.write(zfobj.read(zfobj.namelist()[0]))
  file.close()
  os.remove(fileWOExt + '.srt.zip')
  return 1

for line in sys.argv[1:]:
  if (line[0:2] != '--'):
    findSubtitle(line)
