# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:31:53 2016

@author: Alexey
"""

from blocks import BLOCKS, PLANET_NAMES
from util.tech import ITEM_NAMES, ITEMS
from encryption import decryptor
import sys
from pprint import pprint

game_name = sys.argv[1]

planets = []
xy_blocks = decryptor.readFile(game_name + '.xy')
for block in xy_blocks:
    if block.typeId == 7:
        planets = {pl['id']: pl['name'] for pl in block.planets}

game_data = decryptor.readFile(game_name + '.M1')
for block in game_data:
    if block.typeId in [13, 14]:
        if block['PlanetIDAndOwnerID']['OwnerID'] == 0:
            print planets[block['PlanetIDAndOwnerID']['PlanetID']], block.typeId
            #pprint(block.params)
            if 'Installations' in block.params:
                p = block['Installations']
                print 'Mines: %s Factories: %s' % (p['Mines'], p['Factories'])
        pass
    elif block.typeId == 26:
        pp = block.params
        print pp['Name']
        p = pp['ShipSlot']
        for i in xrange(pp['SlotCount']):
            itemId = p['ItemID'][i]
            itemCat = p['ItemCategory'][i]
            itemCount = p['ItemCount'][i]
            if itemCount == 0:
                continue
            if itemCat in ITEMS:
                print '-'*5, ITEM_NAMES[itemCat],
                if itemId < len(ITEMS[itemCat]):
                    print ITEMS[itemCat][itemId],
                else:
                    print itemId,
            else:
                print '-'*5, itemCat, itemId, 
            print itemCount

            
        
    #else:
    #    print BLOCKS[block.typeId]
    
            