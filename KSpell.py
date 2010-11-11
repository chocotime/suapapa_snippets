# -*- coding: cp949 -*-
from urllib2 import urlopen
from ClientForm import ParseResponse
from BeautifulSoup import NavigableString
from BeautifulSoup import BeautifulSoup as BS

def isStringInTD(text):
    if isinstance(text, NavigableString) and ('%s'%text).strip():
        return True
    else:
        return False

def parseHtmlResult(htmlResult):
    soup = BS(htmlResult)
    tables = soup.findAll('table')
    #print len(tables)
    if len(tables) == 1:
        return None
    table = tables[1]
    trs = table.findAll('tr')
    #print len(trs)
    correctTable = []
    for line in trs[1:]:
        words = line.findAll(text=lambda text:isStringInTD(text))
        correctTable.append(['%s'%words[0],'%s'%words[1]])
    return correctTable

def kSpell(inStr,encoding='cp949'):
    #print 'in:',inStr
    if not encoding == 'cp949':
        inStr = (inStr.decode(encoding)).encode('cp949')
    response = urlopen("http://164.125.36.47/urimal-spellcheck.html")
    forms = ParseResponse(response, backwards_compat=False)
    response.close()
    form = forms[0]
    form["text1"]=inStr
    htmlResult = urlopen(form.click()).read()
    if not htmlResult.strip():
	    return ''
    correctTable = parseHtmlResult(htmlResult.decode('cp949'))
    if not correctTable:
        return inStr
    uniInStr = inStr.decode('cp949')
    for correct in correctTable:
        uniInStr = uniInStr.replace(correct[0],correct[1])
        
    return uniInStr.encode(encoding)


if __name__ =='__main__':
    print kSpell('감자가 빠진 채로 만들어짐.')
    print kSpell('아버지가 방에 들어가신다')
    print kSpell('아 버지가방에들어가신다')
    print kSpell('아버지 가방에들어가신다')
    print kSpell('아버지 가방에들 어가신다')
