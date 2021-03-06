#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# gom_sub.py : search subscript(like smi or srt) on the Gom Subtitle PDS;
# http://gom.gomtv.com/jmdb/index.html
#
# Installation: put this file under ~/.nautilus/python-extensions/
#
# Copyright (C) 2010 by Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import urllib
import webbrowser

GOM_SUB_ADDR = "http://search.gomtv.com/searchjm.gom?whr=7600&spage=0&preface=0&key=%s"

HAS_NAUTILUS = True
try:
    import nautilus
    # place this script under ~/.nautilus/python-extensions/
except:
    # maybe we run this script on terminal
    HAS_NAUTILUS = False


def querySub(searchKey):
    return GOM_SUB_ADDR%\
        urllib.quote_plus(searchKey.decode("utf-8").encode("cp949"))


def searchGomSubPDS(movieName):
    if not movieName.rfind('.') == -1:
        movieName = movieName[:movieName.rfind('.')] # chop the ext.

#        if os.path.exists(movieName+'.smi')\
#            or os.path.exists(movieName+'.srt'):
#            print("Seems like u already have the sub.")

    # increase the chance
    movieName = movieName.replace('.', ' ')
    movieName = movieName.replace('_', ' ')
    movieName = movieName.replace('-', ' ')

    sl = movieName.split()
    while sl:
        testAddr = querySub(' '.join(sl)) 
        # print "Trying %s"%testAddr
        tempSite = urllib.urlopen(testAddr)
        tempDoc = tempSite.read(-1)

        # check if there r any subtitle found.
        if tempDoc.find("<div id='search_failed_smi'>") == -1:
            webbrowser.open(testAddr)
            return True

        # our search key was too long. let's chop more!
        sl = sl[:-1]

    # we are in trouble :$
    print("Give up! no subtitle found.")
    return False

if HAS_NAUTILUS:
    class GomSubExtension(nautilus.MenuProvider):
        def __init__(self):
            pass
        
        def menu_activate_cb(self, menu, file):
            if file.is_gone():
                return
             
            # Strip leading file://
            filename = urllib.unquote(file.get_uri()[7:])
            result = searchGomSubPDS(os.path.basename(filename))
            if not result:
                os.system('zenity --error --title="자막검색" --text="찾지 못했습니다."')
            
        def get_file_items(self, window, files):
            if len(files) != 1:
                return

            file = files[0]

            if not "video/" in file.get_mime_type():
                 return

            if file.get_uri_scheme() != 'file':
                return

            item = nautilus.MenuItem('Nautilus::search_gom_sub_pds',
                                     '자막 검색',
                                     '곰 자막 자료실 검색')
            item.connect('activate', self.menu_activate_cb, file)
            return item,

if __name__ == "__main__":
    try:
        movieName = os.path.basename(sys.argv[1])
    except IndexError:
        print "Usage: %s [the_movie_file_name]"%sys.argv[0]
        sys.exit(1)

    if searchGomSubPDS(movieName):
        sys.exit(0)
    else:
        sys.exit(1)

# vim: et sw=4
