#!/usr/bin/env python
# -*- coding: utf-8 -*-

# raw2HDR.py: a simple scpit for make High Dynamic Ranage Image from 
#             single raw file using ufraw-batch and enfuse.
# Copyright (c) 2008 Homin Lee <ff4500@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os, sys

def _err(errStr):
    sys.stderr.write('ERR!! : '+errStr+'\n')
    sys.exit(1)

def _parseEVRange(minEV, maxEV, step):
    start = minEV
    end = maxEV + step
    if step < 0.1:
        _err('step must bigger then 0.1')
    if minEV >= maxEV:
        _err('maxEV must bigger then minEV')
    L = []
    while 1:
        next = start+len(L) * step
        if step > 0 and next > maxEV:
            break
        L.append('%0.1f'%next)
    return L

def _makeTempTiffNames(evList, inputName):
    dirName = os.path.dirname(inputName)
    baseName = os.path.basename(inputName)
    fileName, _, _ = baseName.rpartition('.')
    L =[]
    for evStr in evList:
        evNum = eval(evStr)
        if evNum < 0:
            evStr = evStr.replace('-','N')
        elif evNum > 0:
            evStr = 'P'+evStr
        evStr = evStr.replace('.','')
        newBaseName = fileName+'_'+evStr+'.tiff'
        L.append(os.path.join(dirName, newBaseName))
    return L

def _execCmd(cmd):
    print '>>',cmd
    ret = os.system(cmd)
    if not ret==0:
        _err('something wrong while running cmd :\n%s'%cmd)

def main():
    from optparse import OptionParser as OptPsr
    usage = "usage: %prog [opitons] input.raw "
    optPsr = OptPsr(usage)
    optPsr.add_option('-o', '--output', type='string', help='output image name')
    optPsr.add_option('-m', '--minEV', type='float', help='min EV value; default=-3', default='-3')
    optPsr.add_option('-M', '--maxEV', type='float', help='max EV value; default=3', default='3')
    optPsr.add_option('-s', '--step', type='float', help='EV step; default=1', default='1')
    optPsr.add_option('-t', '--deleteTemps', action='store_true', help='delete temp tiffs', default=False)
    optPsr.add_option('', '--ufraw', type='string', help='location of ufraw-batch; default=ufraw-batch', default='ufraw-batch')
    optPsr.add_option('', '--enfuse', type='string', help='location of enfuse; default=enfuse', default='enfuse')
    optPsr.add_option('', '--exiftool', type='string', help='location of exiftool; default=exiftool', default='exiftool')
    (opts, args) = optPsr.parse_args()
    if not args:
        _err('must specify input raw image file')
    evRange = _parseEVRange(opts.minEV, opts.maxEV, opts.step)
    inputRaws = args
    for inputRaw in inputRaws:
        ## make multi exposed image from one raw input.
        tempTiffs = _makeTempTiffNames(evRange, inputRaw)
        for i in range(len(evRange)):
            tempTiff = tempTiffs[i]
            if not os.path.exists(tempTiff):
                #cmd = '%s --create-id=no --out-type=tiff8 --exposure=%s --output=%s %s'%\
                cmd = '%s --create-id=no --out-type=tiff --exposure=%s --out-depth=8 --shrink=1 --output=%s %s'%\
                      (opts.ufraw, evRange[i], tempTiff, inputRaw)
                _execCmd(cmd)

        ## enfuse it!
        if not opts.output:
            dirName = os.path.dirname(inputRaw)
            baseName = os.path.basename(inputRaw)
            fileName, _, _ = baseName.rpartition('.')
            output = os.path.join(dirName, fileName+'_enfused.tiff')
        else:
            output = opts.output        
        cmd = '%s -o %s %s '%\
              (opts.enfuse, output, ' '.join(tempTiffs))
        _execCmd(cmd)

        ## insert exif from input raw to enfused image
        if inputRaw.endswith('.ufraw'):
            import re
            ptrn = re.compile('<InputFilename>(.*)</InputFilename>')
            for line in open(inputRaw):
                rawSource = ptrn.findall(line)
                if rawSource:
                    inputRaw = rawSource[0]
                    break
            
        #cmd = '%s -tagsfromfile %s -exif:all %s'%\
        cmd = '%s -tagsfromfile "%s" -exif:all "%s"'%\
              (opts.exiftool, inputRaw, output)
        _execCmd(cmd)
        os.remove(output+'_original')

        ## delete temp multi exposed tiffs
        if opts.deleteTemps:
            for tempTiff in tempTiffs:
                print 'delete %s'%tempTiff
                os.remove(tempTiff)
        

if __name__ == '__main__':
    main()

