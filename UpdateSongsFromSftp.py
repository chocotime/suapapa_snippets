#!/usr/bin/env python

# UpdateSongsFromSftp.py: update songs in your mp3 player via sftp
#
# Copyright (c) 2007-2009 Homin Lee <ff4500@gmail.com>
# License: LGPL (see lgpl.txt)
#
# THIS PROGRAM COMES WITH NO WARRANTY

import sys, re, time
import os, glob, paramiko

# Change following sftp settings to your environment
SSH_ADDR = 'user.sshserver.net'
SSH_PORT = 2222 # must be int for port num
SSH_USERNAME = 'user_id'
#SSH_DIR = 'TBSEFMArchive/OOB/'
SSH_DIR = 'EbsRadioArchive/UnplugEarEng/'

def dotint(v):
    dotstr = str(v)
    left = dotstr[:len(dotstr)%3]
    right = re.findall('...', dotstr[len(dotstr)%3:])
    if left:
        right.insert(0, left)
    return ','.join(right)

class ConsoleSlider:
    def __init__ (self, max, initpos):
        self.barfill = -1
        self.max = max
        self.initpos = initpos
        self.sessmax = max - initpos
        try:
            import fcntl, termios, struct
            s = struct.pack("HHHH", 0, 0, 0, 0)
            self.cols = struct.unpack("HHHH", fcntl.ioctl(sys.stdout.fileno(),
            termios.TIOCGWINSZ, s))[1]
        except:
            self.cols = 78
        self.barsize = self.cols - 12 # 4(percent) + 2([]) + 4(spaces) + 2(endmark)
        self.barsize -= len(dotint(max)) # done value
        self.barfmt = '\r%%-4s[%%s>%%s] %%-%ds ' % len(dotint(max))
        self.barsize -= 22
        self.st = time.time()
        self.update(0)

    def update (self, value, *ext):
        newfill = int( float(value+self.initpos) * self.barsize / self.max )
        if 1: # newfill != self.barfill:
            self.barfill = newfill
            sys.stdout.write(self.barfmt %
                ( str(int(newfill * 100 / self.barsize))+'%',
                '='*(newfill - 1),
                ' '*(self.barsize-newfill),
                dotint(value) ) )

        if value * 30 >= self.sessmax: # over 3%
            elapsed = time.time() - self.st
            estimated = int(float(self.sessmax) / value * elapsed - elapsed)
            sys.stdout.write("%7.2fK/s ETA %02d:%02d" %
                ( float(value) / elapsed / 1024,
                int(estimated/60),
                int(estimated%60) ) ) # int is for py3k
        sys.stdout.flush()

    def end (self):
        print
        
progressBar = None
def progressCb(curr, total):
    global progressBar
    
    if not progressBar:
        progressBar = ConsoleSlider(total, curr)
    else:
        progressBar.update(curr)


def downloadMP3():
    global progressBar
    
    print ("== get private ssh key ==")
    try:
        pk = paramiko.Agent().get_keys()[0]
    except:
        print ("no key found! don't you forgot 'ssh-add'?")
        sys.exit(1)
    
    print ("== connect sftp server ==")
    t = paramiko.Transport((SSH_ADDR, SSH_PORT))
    t.connect(username=SSH_USERNAME, pkey=pk)
    sftpC = paramiko.SFTPClient.from_transport(t)
    sftpC.chdir(SSH_DIR)
    remoteMP3s = sftpC.listdir()

    print ("== delete Old mp3s ==")
    localMP3s = glob.glob('*.mp3')
    for mp3 in localMP3s:
        os.remove(mp3)
        print ("  >> %s deleted"%mp3)

    print ("== download lasted mp3s ==")
    if localMP3s:
        lastMP3inLocal = max(localMP3s)   
        downloadMP3s = filter(lambda x: x>lastMP3inLocal, remoteMP3s)
    else:
        downloadMP3s = remoteMP3s
    downloadMP3s.sort()

    totalCnt = len(downloadMP3s)
    currCnt = 0
    for mp3 in downloadMP3s:
        progressBar = None
        currCnt += 1
        print (" >> downloading %s [%d/%d]"%(mp3, currCnt, totalCnt))
        sftpC.get(mp3, mp3, progressCb)
        progressBar.end()

    sftpC.close()
    t.close()
    print ("== all done ==")

if __name__=='__main__':
    downloadMP3()
