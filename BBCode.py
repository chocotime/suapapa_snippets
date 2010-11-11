# -*- coding: cp949 -*-
import re

_BBcodeRexPatterns = [
    [ re.compile("&"), r"&"],
    [ re.compile("<"), r"<" ],
    [ re.compile(">"), r">" ],
    [ re.compile("'"), r'&apos;' ],
    [ re.compile('"'), r'"' ],
    [ re.compile('(\n|\r|\n)'), r'<br/>\1'],
    [ re.compile('\[[Bb]\](.+?)\[/[Bb]\]'), r'<b>\1</b>' ],
    [ re.compile('\[[Ii]\](.+?)\[/[Ii]\]'), r'<i>\1</i>' ],
    [ re.compile('\[[Uu]\](.+?)\[/[Uu]\]'), r'<u>\1</u>' ],
    [ re.compile('\[[Hh]([1-6])\](.+?)\[/[Hh]\1\]'), r'<h\1>\2</h\1>' ],
    [ re.compile('(\s|^)(http|ftp)(://[^\s:]+)'), r'\1<a href="\2\3">\2\3</a>' ],
    [ re.compile('(\s|^)(www\.[^\s/]+\.[a-zA-Z]{2,4}(/[^\s/]*)*)'), r'\1<a href="http://\2">\2</a>' ],
    [ re.compile('(\s|^)(ftp\.[^\s/]+\.[a-zA-Z]{2,4}(/[^\s/]*)*)'), r'\1<a href="ftp://\2">\2</a>' ],
    [ re.compile('(\s|^)([a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,4})'), r'\1<a href="mailto:\2">\2</a>' ],
    [ re.compile('\[[Uu][Rr][Ll]\](.+?)\[/[Uu][Rr][Ll]\]'), r'<a href="\1">\1</a>' ],
    [ re.compile('\[[Uu][Rr][Ll]=([^\]]+)\](.+?)\[/[Uu][Rr][Ll]\]'), r'<a href="\1">\2</a>'],
    [ re.compile('\[[Ii][Mm][Gg]\](.+?\.(png|gif|jpe?g|svg))\[/[Ii][Mm][Gg]\]'), r'<img src="\1"/>' ]]

def decodeBBcode(bbStr):
        for fromPtrn, toPtrn in _BBcodeRexPatterns:
                for p in fromPtrn.finditer(bbStr):
                        fromStr = p.group()
                        toStr = p.expand(toPtrn)
                        bbStr = bbStr.replace(fromStr,toStr)
        return bbStr

if __name__ == '__main__':
    bbStr = '[url=http://www.python.org]파이썬마을[/url]\n[url=http://www.python.org]파이썬마을2[/url]'
    print decodeBBcode(bbStr)

