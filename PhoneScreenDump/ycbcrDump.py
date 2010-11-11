#!/usr/bin/python

def CLIPIT(a):
    a = int(a)
    if ((a<0)or(a>255)):
        if a<0:
            return 0
        else:
            return 255
    else:
        return a

def CLIP_32bit(a):
    if a < 0:
        sign = False
    else:
        sign = True
    a = abs(a)
    clipa = a&0xffffffff
    if not a == clipa:
        print 'some value clipped 0x%x => 0x%x'%(a,clipa)
    if sign:
        return clipa
    else:
        return -clipa
    
    
    
def YUV2RGB_ipl(luma,cb,cr):
    ycbcr_convert = [8, 25803, -3071, -7672, 30399, 12]
    rc = (ycbcr_convert[0]*(cb-128) + ycbcr_convert[1]*(cr-128))*4 + 0x8000
    gc = (ycbcr_convert[2]*(cb-128) + ycbcr_convert[3]*(cr-128))*4 + 0x8000
    bc = (ycbcr_convert[4]*(cb-128) + ycbcr_convert[5]*(cr-128))*4 + 0x8000

    r = CLIPIT(luma + (rc>>16)) # /65535
    g = CLIPIT(luma + (gc>>16))
    b = CLIPIT(luma + (bc>>16))
    return r,g,b

def YUV2RGB_homin(luma,cb,cr):
    r = CLIPIT(luma + 1.402*(cr-128))
    g = CLIPIT(luma - 0.344*(cb-128) - 0.715*(cr-128))
    b = CLIPIT(luma + 1.773*(cb-128))
    return r,g,b

def YUV2RGB_homin_ipl(luma,cb,cr):
    ycbcr_convert = [0, 358, -88, -183, 453, 0]
    rc = (ycbcr_convert[0]*(cb-128) + ycbcr_convert[1]*(cr-128))
    gc = (ycbcr_convert[2]*(cb-128) + ycbcr_convert[3]*(cr-128))
    bc = (ycbcr_convert[4]*(cb-128) + ycbcr_convert[5]*(cr-128))

    rc = CLIP_32bit(rc)
    gc = CLIP_32bit(gc)
    bc = CLIP_32bit(bc)

    r = CLIPIT(luma + (rc>>8)) # /65535
    g = CLIPIT(luma + (gc>>8))
    b = CLIPIT(luma + (bc>>8))
    return r,g,b


def YUV2RGB_gray(luma,cb,cr):
    r = luma
    g = luma
    b = luma
    return r,g,b

def YUV2RGB_cb(luma,cb,cr):
    r = cb
    g = cb
    b = cb
    return r,g,b
def YUV2RGB_cr(luma,cb,cr):
    r = cr
    g = cr
    b = cr
    return r,g,b
def makeBmp(xw, yw, dumpFile, offset):
    import Image
    print 'makeBmp :'+dumpFile,
    xW = int(xw,10)
    yW = int(yw,10)
    fp = open(dumpFile, 'rb')
    img = Image.new('RGB' ,(xW,yW), 0)
    fp.seek(offset)
    w = fp.read(4)
    x=0
    y=0

    #YUV2RGB = YUV2RGB_cr
    #YUV2RGB = YUV2RGB_gray
    YUV2RGB = YUV2RGB_homin_ipl
    try:
        while(w):
            luma1 = ord(w[0])
            cb = ord(w[1])
            luma2 = ord(w[2])
            cr = ord(w[3])

            r,g,b = YUV2RGB(luma1,cb,cr)

            img.putpixel((x,y),(r,g,b))
            x+=1
            if (x >= xW):
                x=0
                y+=1

            r,g,b = YUV2RGB(luma2,cb,cr)

            img.putpixel((x,y),(r,g,b))
            x+=1
            if (x >= xW):
                x=0
                y+=1

            w=fp.read(4)
        img.save(dumpFile+'.bmp')
        print '--> '+dumpFile+'.bmp'
    except IndexError:
        img.save(dumpFile+'.bmp')
        print '--> '+dumpFile+'.bmp'
        
    
def makeBmps(xW, yW, dumpFiles, offset):
    import glob
    for dumpFile in glob.glob(dumpFiles):
        makeBmp(xW, yW, dumpFile, offset)

if __name__ == '__main__':
    import sys
    print '### make BMP from trace dump ###'
    print '###      created by hominLee ###'
    print '\t1. make trace dump of screen'
    print '\t\td.save.b c:\screen02.dump 0x1459E52C--0x145A652C'
    print '\t2. make bmp from dump files'
    print '\t\t..>'+sys.argv[0]+' *.dump'
    try:
        xWidth = sys.argv[1]
        yWidth = sys.argv[2]
        dumpFiles = sys.argv[3]
        offset = 0
        if len(sys.argv) == 5:
            offset = int(sys.argv[4])
        makeBmps(xWidth, yWidth, dumpFiles, offset)
    except IndexError:
        print '!!Error :  Check args!!'
        print '\t..>'+sys.argv[0]+' xWidth yWidth files'
