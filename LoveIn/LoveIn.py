#!/usr/bin/env python
# -*- coding: cp949 -*-

# LoveIn.py: calurate love match percentage
#
# Copyright (c) 2007-2008 Homin Lee <ff4500@gmail.com>
# License: LGPL (see lgpl.txt)
#
# THIS PROGRAM COMES WITH NO WARRANTY

import hangul

_ja = hangul.Jaeum
_mo = hangul.Moeum

_dicStrokeCnt = {
    _ja.G : 1,
    _ja.N : 1,
    _ja.D : 2,
    _ja.L : 3,
    _ja.M : 3,
    _ja.B : 4,
    _ja.S : 2,
    _ja.NG : 1,
    _ja.J : 3,
    _ja.C : 4,
    _ja.K : 2,
    _ja.T : 3,
    _ja.P : 4,
    _ja.H : 3,
    _mo.A : 2,
    _mo.YA : 3,
    _mo.EO :2,
    _mo.YEO :3,
    _mo.O :2,
    _mo.YO :3,
    _mo.U :2,
    _mo.YU :3,
    _mo.EU :1,
    _mo.I :1
}
    
def _getStrokeCnt(koChr):
    ''' �ѱ� �� ������ ȹ���� ��ȯ '''
    strokeCnt = 0
    f, m, l = hangul.split(koChr)
    for ja in (f, l):
        if not ja: continue #������ ���� ���
        if ja in _ja.MultiElement.keys():
            for s in _ja.MultiElement[ja]:
                strokeCnt += _dicStrokeCnt[s]
        else:
            strokeCnt += _dicStrokeCnt[ja]
    if m in _mo.MultiElement.keys():
        for s in _mo.MultiElement[m]:
            strokeCnt += _dicStrokeCnt[s]
    else:
        strokeCnt += _dicStrokeCnt[m]
    return strokeCnt

def _getInt(liNum):
    ''' ���� �迭�� ���ڷ� ���ؼ� ��ȯ '''
    iNum = 0
    for i in liNum:
        iNum *= 10
        iNum += i
    return iNum
        
def _doLoveSum(liNum):
    ''' ȹ�� ����Ʈ�� �޾� 100���ϰ� �� ������ �ٿ��� '''
    # TODO: center alignment
    print liNum
    if _getInt(liNum) > 100:
        retNumLi = []
        for i in range(len(liNum)-1):
            retNumLi.append((liNum[i]+liNum[i+1])%10)
        return _doLoveSum(retNumLi)
    else:
        return _getInt(liNum)

def matchByName (name1, name2, encoding = None):
    ''' �� �̸��� ������ ǥ�� '''
    if encoding:
        name1 = name1.decode(encoding)
        name2 = name2.decode(encoding)
        
    liNamePool = []
    for i in range(len(name1)+len(name2)):
        if i % 2 == 0:
            liNamePool.append(name1[i/2])
        else:
            liNamePool.append(name2[i/2])
        
    print '  '.join(liNamePool)
    loveSum = _doLoveSum(map(_getStrokeCnt, liNamePool))
    print loveSum, '%'

def _test():
    matchByName ("������".decode('cp949'), "�Ѱ���".decode('cp949'))
    matchByName ("������".decode('cp949'), "���ٿ�".decode('cp949'))
    matchByName ("������".decode('cp949'), "����".decode('cp949'))
    matchByName ("�̸��".decode('cp949'), "������".decode('cp949'))
    matchByName ("����", "����", "cp949")
    
if __name__ == '__main__':
    _test()        
