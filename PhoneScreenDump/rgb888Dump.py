def get1Byte(data):
	if data < 0:
		return 0
	if data > 255:
		return 255
	return int(data)

def getRGB(Y, Cb, Cr):
	R = Y     + 1.40200 * (Cr - 0x80) 
	G = Y - 0.34414 * (Cb - 0x80) - 0.71414 * (Cr - 0x80) 
	B = Y + 1.77200 * (Cb - 0x80)
	return get1Byte(R),get1Byte(G),get1Byte(B)

def WORDtoRGB_2(YCbCr):
	s_Y = (YCbCr & 0xff0000) >> (4*4)
	s_Cb = (YCbCr & 0x00ff00) >> (2*4)
	s_Cr = (YCbCr & 0x0000ff)
	return getRGB(s_Y, s_Cb, s_Cr)



def WORDtoRGB(w):
    r=(w&0xff0000)>>16
    g=(w&0x00ff00)>>8
    b=(w&0x0000ff)
    #return r,g,b
    #return b,g,r
    #return r,b,g
    return b,r,g

def makeBmp(xw, yw, dumpFile):
    import Image
    print 'makeBmp :'+dumpFile,
    xW = int(xw,10)
    yW = int(yw,10)
    fp = open(dumpFile, 'rb')
    img = Image.new('RGB' ,(xW,yW), 0)
    #fp.seek(40)
    w = fp.read(3)
    x=0
    y=0
    try:
        while(w):
            #print ord(w[1]),ord(w[0]), WORDtoRGB(ord(w[1]),ord(w[0]))
            #img.putpixel((x,y),WORDtoRGB((ord(w[1])<<8)+ord(w[0])))
            img.putpixel((x,y),(ord(w[0]),ord(w[1]),ord(w[2])))
            #img.putpixel((x,y),WORDtoRGB((ord(w[0])<<8)+ord(w[1])))
            x+=1
            if (x >= xW):
                x=0
                y+=1
            w=fp.read(3)
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
