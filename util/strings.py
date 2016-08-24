# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 10:10:31 2016

@author: Alexey
"""

hexDigits = "0123456789ABCDEF"
encodesOneByte = " aehilnorst"
ENCODES = {'B': "ABCDEFGHIJKLMNOP",
           'C': "QRSTUVWXYZ012345",
           'D': "6789bcdfgjkmpquv",
           'E': "wxyz+-,!.?:;'*%$"
           }


def nibbleToChar(b):
    i1 = (b&0xff) + ord('0');
    i2 = (b&0xff) + ord('A') - 10;
    i3 = (b&0xff) + ord('a') - 10;
    if i1 >= ord('0') and i1 <= ord('9'):
        return i1
    elif i2 >= ord('A') and i2 <= ord('F'):
        return i2
    elif i3 >= ord('a') and i3 <= ord('f'):
        return i3
    return ' '


def decodeBytesForStarsString(res):
    result = []
    hexChars = []
    num = []
    for i in xrange(len(res)):
        b = res[i]
        b1 = (b & 0xff) >> 4
        b2 = (b & 0xff) % 16
        hexChars.append(nibbleToChar(b1))
        hexChars.append(nibbleToChar(b2))
        num.extend([b1, b2])
    ipos = 0
    while ipos < len(hexChars):
        firstChar = chr(hexChars[ipos])
        if firstChar in ENCODES:
            ipos = ipos + 1
            b2 = num[ipos]
            result.append(ENCODES[firstChar][b2])
        elif firstChar != 'F':
            index = num[ipos]
            result.append(encodesOneByte[index])
        ipos = ipos + 1
    return ''.join(result)

