#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CurveError(Exception):
    """Errors during processing curve"""
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg) 


class Curve:
    """Curve Interface"""
    def __init__(self, fileName = None):
        if fileName:
            self.load(fileName)
        else:
            self._clear()
        
    def _clear(self):
        self._level = []
        self._red = []
        self._green = []
        self._blue = []
        self._alpha = []
        
    def getPointsOfChannel(self, channel):
        if channel == 'L':
            channelPoints = self._level
        elif channel == 'R':
            channelPoints = self._red
        elif channel == 'G':
            channelPoints = self._green
        elif channel == 'B':
            channelPoints = self._blue
        else:
            channelPoints = []

        if len(channelPoints) < 3:
            return []
        else:
            return channelPoints
    
    def getSizeOfChannel(self, channel):
        return len(self.getPointsOfChannel(channel))
    
    def load(self, fileName):
        self._clear()
        self._fileName = fileName


class GimpCurve(Curve):
    """Curve from Gimp curve file"""
    def _parseCurveStr(self, line):
        strCurve = line.split()
        iCurve = map(int, strCurve)
        while (-1 in iCurve):
            iCurve.remove(-1)
        return zip(iCurve[::2], iCurve[1::2])
        
    def load(self, fileName):
        Curve.load(self, fileName)
        curvefile = open(u''+fileName,'r')
        lines = curvefile.readlines( )
        if lines[0].strip() == "# GIMP Curves File":
            self._level = self._parseCurveStr( lines[1] )
            self._red = self._parseCurveStr( lines[2] )
            self._green = self._parseCurveStr( lines[3] )
            self._blue = self._parseCurveStr( lines[4] )
        else:
            raise CurveError(_("This is not a GIMP Curves File"))
        curvefile.close()  


from struct import unpack
class PhotoshopCurve(Curve):
    """Curve from Photoshop curve file(.acv)"""
    def load(self, fileName):
        Curve.load(self, fileName)
        if not fileName.upper().endswith('.ACV'):
            raise CurveError(_("This is not Photoshop Curves File"))
        curvefile = open(u''+fileName,'rb')
        _, curveCnt = unpack(">hh", curvefile.read(4))
        if curveCnt > 5:
            raise CurveError(_("More than 5 curves, output may be invalid!"))

        chanCnt = 1
        for chanCrv in [self._level, self._red, self._green, self._blue, self._alpha]:
            pointCnt = unpack(">h", curvefile.read(2))[0]
            #if pointCnt > 17:
            #    raise CurveError(_("%d in curve %d, some points will be ignored")%(pointCnt, chanCnt))
            for p in range(0, pointCnt):
                y, x = unpack(">hh", curvefile.read(4))
                chanCrv.append((x,y))
            chanCnt += 1
            if (chanCnt > curveCnt):
                break
        curvefile.close()

class NikonCurve(Curve):
    """Curve from Photoshop curve file(.ntc)"""
    pass

def _isGimpCurve(curveFile):
    rp = open(u''+curveFile,'r')
    firstLine = rp.readline( )
    rp.close()
    if firstLine.strip() == "# GIMP Curves File":
        return True
    return False
    
def _isPhotoshopCurve(curveFile):
    if curveFile.upper().endswith('.ACV'):
        return True
    return False

def getCurveFrom(curveFile):
    """Retrun appropriate Curve instance by curve file name"""
    if _isGimpCurve(curveFile):
        return GimpCurve(curveFile)
    elif _isPhotoshopCurve(curveFile):
        return PhotoshopCurve(curveFile)
    else:
        #print curveFile
        return None
    
if __name__ == '__main__':
    import os
    crv = Curve()
    print crv.getPointsOfChannel('R')
    crv = getCurveFrom(os.path.join("curve_samples", "HeyJey_CP_RED"))
    print crv._fileName
    print crv.getPointsOfChannel('R')
    crv = getCurveFrom(os.path.join("curve_samples", "FilmLike2.acv"))
    print crv._fileName
    print crv.getPointsOfChannel('L')

