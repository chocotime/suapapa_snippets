#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# screenshot_n1.py - description
#
# Copyright (C) 2011 Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

FRAME_NAME = 'n1_templete.png'
PASTE_XY = (46,129)
PASTE_SIZE = (480, 800)
PASTE_MAP = PASTE_XY + (PASTE_XY[0]+PASTE_SIZE[0], PASTE_XY[1]+PASTE_SIZE[1])
TEMP_CAPTURE = "__capture.png"

SCREENSHOT2 = 'screenshot2'

import Image
import os

def pasteWithGlare(imgFrm, imgCap):
    imgRet = Image.new('RGBA', imgFrm.size)
    imgRet.paste(imgCap, PASTE_MAP)
    imgRet.paste(imgFrm, (0, 0) + imgFrm.size, imgFrm)
    return imgRet

def pasteWithNoGlare(imgFrm, imgCap):
    imgFrm.paste(imgCap, PASTE_MAP)
    return imgFrm

if __name__ == '__main__':
    from optparse import OptionParser

    optPsr = OptionParser("usage: %prog [-g] [-rN] -o CapturedImgName")
    optPsr.add_option('-o', '--out', type='string', help='output image file name')
    optPsr.add_option('-r', '--rotate', type='int', help='rotate degree')
    optPsr.add_option('-g', '--glare', action='store_true', default=False,
            help = 'glare effect over the screen')
    (opts, args) = optPsr.parse_args()

    if not opts.out:
        optPsr.error("no output name")

    imgFrm = Image.open(FRAME_NAME)
    os.system(SCREENSHOT2 + ' -d %s'%TEMP_CAPTURE)
    imgCap = Image.open(TEMP_CAPTURE)
    
    if opts.glare:
        imgRet = pasteWithGlare(imgFrm, imgCap)
    else:
        imgRet = pasteWithNoGlare(imgFrm, imgCap)

    if opts.rotate:
        imgRet = imgRet.rotate(-opts.rotate)

    imgRet.save(opts.out)

# vim: et sw=4 fenc=utf-8:
