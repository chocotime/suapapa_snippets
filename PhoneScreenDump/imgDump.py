def WORDtoRGB(w):
    r=(w>>11) *8
    g=((w>>5)&0x3f)*4
    b=(w&0x1f)*8
    r = r*255/248
    g = g*255/252
    b = b*255/248
    return r,g,b

def makeBmp(xw, yw, dumpFile):
    import Image
    print 'makeBmp :'+dumpFile,
    xW = int(xw,10)
    yW = int(yw,10)
    fp = open(dumpFile, 'rb')
    img = Image.new('RGB' ,(xW,yW), 0)
    w = fp.read(2)
    x=0
    y=0
    try:
        while(w):
            #print ord(w[1]),ord(w[0]), WORDtoRGB(ord(w[1]),ord(w[0]))
            img.putpixel((x,y),WORDtoRGB((ord(w[1])<<8)+ord(w[0])))
            x+=1
            if (x >= xW):
                x=0
                y+=1
            w=fp.read(2)
        img.save(dumpFile+'.bmp')
        print '--> '+dumpFile+'.bmp'
    except IndexError:
        img.save(dumpFile+'.bmp')
        print '--> '+dumpFile+'.bmp'
        
    
def makeBmps(xW, yW, dumpFiles):
    import glob
    for dumpFile in glob.glob(dumpFiles):
        makeBmp(xW, yW, dumpFile)

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
        makeBmps(xWidth, yWidth, dumpFiles)
    except IndexError:
        print '!!Error :  Check args!!'
        print '\t..>'+sys.argv[0]+' xWidth yWidth files'
