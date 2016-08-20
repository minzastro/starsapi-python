#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 18:29:36 2016

@author: mints
"""
from util import *
from blocks.Block import Block
from lxml import etree
from os import path

def get_bits(inp, size, low, length):
    return (inp & (2**(size-low)-1)) >> (size - low - length)

def evaluate(params, expression):
    expression = expression.replace('^', '**')
    while '[' in expression:
        left = expression.index('[')
        right = expression.index(']')
        keys = expression[left+1:right].split('/')
        if keys[0] in params:
            value = params[keys[0]]
            if type(value) == dict:
                if len(keys) == 1:
                    value = value['']
                elif keys[1] in value:
                    value = params[keys[0]][keys[1]]
                else:
                    value = 0
        else:
            value = 0
        expression = expression.replace(expression[left:right+1], str(value))
    if expression.startswith('iif'):
        cond, ok, other = expression[4:-1].split(',')
        cond = cond.replace('=', '==')
        if eval(cond):
            return ok
        else:
            return other
    else:
        return eval(expression)


class ArbitraryBlock(Block):
    def __init__(self, typeId, size, data):
        Block.__init__(self, typeId, size, data)
        self.params = {}
        self.kids = {}
        self.data = data
        self.typeId = typeId
        self.description = ''
        #print typeId
        
    def __getitem__(self, key):
        if key in self.params:
            return self.params[key]
        else:
            raise ValueError('%s not in %s (%s) params' % (key, self.typeId,
                             self.description))
                             
    def parse(self):
        fname = '%s/Structures/Structure%s.xml' % (path.dirname(__file__), self.typeId)
        if path.exists(fname):
            root = etree.parse(fname).getroot()
            self.offset = 0
            self.description = root.attrib.values()[0]
            for element in root.iterchildren():
                self.read_element(element)
        
    def read_element(self, element):
        attrib = element.attrib
        tag = element.tag    
        print tag, attrib,
        if 'bytes' in attrib:
            bytez = int(evaluate(self.params, attrib['bytes']))
            print bytez
            if 'type' in attrib:
                if attrib['type'] == 'text' or attrib['type'] == 'StarsText':
                    content = str(self.data[self.offset:self.offset+bytez])
                    self.offset += bytez
                else:
                    #print self.params, self.typeId
                    raise Exception('Unknown type: %s' % attrib['type'])
            else:
                if bytez == 2:
                    content = read16(self.data, self.offset)
                    self.offset += 2
                elif bytez == 1:
                    content = read8(self.data, self.offset)
                    self.offset += 1
                else:
                    content = readN(self.data, self.offset, bytez)
                    self.offset += bytez
                    
        print "$", content, "$"
        if tag in self.params and type(self.params[tag]) == dict:
            self.params[tag][''] = content
        else:
            self.params[tag] = content
        kids = {'': content}
        ind = 0
        for child in element.getchildren()[::-1]:
            #print '-'*5, '>', child.tag, child.attrib, bytez
            if 'bits' in child.attrib:
                bits = int(child.attrib['bits'])
            else:
                bits = int(child.attrib['Bits'])            
            kids[child.tag] = get_bits(content, int(bytez)*8, ind, bits)
            print child.tag, kids[child.tag]
            ind += bits
        if ind > 0:
            if type(self.params[tag]) == dict:
                self.params[tag].update(kids)
            else:
                self.params[tag] = kids

    def __str__(self):
        return '%s: %s' % (self.description, str(self.params))
 
                
    
