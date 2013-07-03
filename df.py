#!/usr/bin/env python3
import httplib2, os, subprocess, re, urllib
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://bay12games.com/dwarves/older_versions.html')

# all the df releases are wrapped in paragraphs with the 'menu' class
for p in BeautifulSoup(response, parse_only=SoupStrainer('p', attrs={'class':'menu'})):
	
	# get string in <p>, sanitize, and make a dir with this as name
	thisrelease = p.contents[0].string
	stripchars = re.sub('[,()]', '', thisrelease).replace(' ','_')
	os.makedirs(stripchars) 

	# find the downloads and get em
	links = p.findAll('a')
	for a in links:
		thislink = str('http://bay12games.com/dwarves/' + a['href'])
		thisfile = str(stripchars + '/' + a['href'])
		print 'downloading ' + a['href']
		urllib.urlretrieve(thislink, thisfile)

