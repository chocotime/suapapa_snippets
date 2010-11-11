#!/usr/bin/env python
# -*- coding: euc-kr -*-
import urllib
import re
import os
import sys

if __name__ == '__main__':

    boardUrl = 'http://bestgm.bestiz.net/zboard/'
    pageUrlTemplete = boardUrl+'zboard.php?id=singcotest&page=%d&select_arrange=headnum&desc=asc&category=&sn=on&ss=off&sc=off&keyword=꽃사슴&sn1=&divpage=1'
    pages = [1, 2, 3]

    imgCnt = 1

    postUrls = []
    for page in pages:
	pageUrl = pageUrlTemplete%page
	for line in urllib.urlopen(pageUrl).readlines():
	    if ("꽃사슴" in line) and ("a href" in line): #this is song post
		aLink = re.findall(r"<a href=(.*)>(.*?)</a>", line)
		if aLink:
		    url, songName = aLink[0]
		if not "회원노래" in songName:
		    postUrls.append((url, songName))

    songUrls = []
    for url, songName in postUrls:
	postUrl = boardUrl + url.strip('"')
	mp3Founded = False
	songName = songName.replace(':', '_')
	songName = (songName.decode('cp949')).encode(sys.getfilesystemencoding())
	print songName, 

	for line in urllib.urlopen(postUrl).readlines():
	    #songs = re.findall(r'<embed src="(.*\.mp3)">', line)
	    songs = re.findall(r'<embed src=(.*?)>', line)
	    if songs:
		mp3Founded = True
		songUrl =  songs[0].strip('"')
		mp3FileName = songName+'.mp3'
		
		if not os.path.exists(mp3FileName):
		    print "downloading ...",
		    wFp = open(songName+'.mp3', 'wb')
                    print songUrl
		    wFp.write(urllib.urlopen(songUrl).read())
		    wFp.close()
		    print "[OK]"
		else:
		    print "already exists",
		    print "[PASS]"

		break
	if not mp3Founded:
	    print "somthing wrong",
	    print "[FAIL]"
	    print "\tcheck URL :",songUrl

