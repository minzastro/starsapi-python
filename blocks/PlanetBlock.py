#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:16:23 2016

@author: mints
"""

from util import read16, read8

from blocks import PLANET_NAMES
from blocks.Block import Block
from blocks.ArbitraryBlock import ArbitraryBlock

def get_bits(inp, size, low, length):
    return (inp & (2**(size-low)-1)) >> (size - low - length)

class PlanetBlock(Block):
    def __init__(self, typeId, size, data):
        Block.__init__(self, typeId, size, data)
        b = ArbitraryBlock(typeId, size, data)
        b.parse()
        #print b.params
        self.planetNumber = (data[0] & 0xFF) + ((data[1] & 7) << 8)
        self.name = PLANET_NAMES[self.planetNumber]
        self.owner = (data[1] & 0xF8) >> 3
        #print self.planetNumber, self.owner
        boo = read16(data, 0)
        #print get_bits(boo, 16, 0, 5), get_bits(boo, 16, 5, 11)
        
        if self.owner == 31:
            self.owner = -1
        elif self.owner >= 16:
            raise Exception("Unexpected owner: " + self.owner)
        flags = read16(data, 2)
        if (flags & 0x0078) != 0:
            raise Exception("Unexpected planet flags: " + flags)
        if (flags & 0x0100) != 0x0100:
            raise Exception("Unexpected planet flags: " + flags)
        self.isHomeworld = (flags & 0x80) != 0
        self.isInUseOrRobberBaron = (flags & 0x04) != 0
        self.hasEnvironmentInfo = (flags & 0x02) != 0
        self.bitWhichIsOffForRemoteMiningAndRobberBaron = (flags & 0x01) != 0
        self.weirdBit = (flags & 0x8000) != 0
        self.hasRoute = (flags & 0x4000) != 0
        self.hasSurfaceMinerals = (flags & 0x2000) != 0
        self.hasArtifact = (flags & 0x1000) != 0
        self.hasInstallations = (flags & 0x0800) != 0
        self.isTerraformed = (flags & 0x0400) != 0
        self.hasStarbase = (flags & 0x0200) != 0
        index = 4
        if self.hasEnvironmentInfo:
            preEnvironmentLengthByte = data[4]
            if ((preEnvironmentLengthByte & 0xC0) != 0):
                raise Exception("Unexpected bits at data[3]: " + self)
            preEnvironmentLength = 1
            preEnvironmentLength += (preEnvironmentLengthByte & 0x30) >> 4
            preEnvironmentLength += (preEnvironmentLengthByte & 0x0C) >> 2
            preEnvironmentLength += (preEnvironmentLengthByte & 0x03)
            self.fractionalMinConcBytes = data[4:preEnvironmentLength+4]
            index += preEnvironmentLength + 1
            self.ironiumConc = data[index]
            self.boraniumConc = data[index+1]
            self.germaniumConc = data[index+2]
            self.gravity = data[index+3]
            self.temperature = data[index+4]
            self.radiation = data[index+5]
            index = index + 5
            if (self.isTerraformed):
                self.origGravity = data[index+1]
                self.origTemperature = data[index+2]
                self.origRadiation = data[index+3]
                index = index + 3
            if (self.owner >= 0):
                estimatesShort = read16(data, index + 1)
                self.defensesEstimate = estimatesShort / 4096
                self.popEstimate = estimatesShort % 4096
                index += 2
       
    def canSeeEnvironment(self):
        return self.hasEnvironmentInfo + ((self.hasSurfaceMinerals + self.isInUseOrRobberBaron) * (not self.bitWhichIsOffForRemoteMiningAndRobberBaron))


    def __str__(self):
      return """%s - typeId: %d name: %s owner: %s:
""" % (self.__class__.__name__, self.typeId, self.name, self.owner)
