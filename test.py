'''
Created on Jul 19, 2014

@author: raptor
'''
import array
import string

from blocks import BLOCKS, PLANET_NAMES
from encryption import decryptor
import util
import sys
from pprint import pprint


def main():
    starsFile = sys.argv[1]
#     starsFile = "../../../../games/stars27j/games/difficultattempt.h1"
#     starsFile = "../../../../games/stars27j/games/Game.xy"
#     starsFile = "../../../../games/stars27j/games/Game.h1"
#     starsFile = "../../../../games/stars27j/games/Game.m1"
#     starsFile = "../../../../games/stars27j/games/Game.hst"
    
    # Retrieve a list of decrypted blocks from the file
    blocks = decryptor.readFile(starsFile)
    
    # Now do great and amazing things with the blocks!
    print "Printing detected blocks:"
    for block in blocks:
        if block.typeId not in BLOCKS:
            print 'Unknown block:', block.typeId
            continue
        #print BLOCKS[block.typeId], block.typeId
        if block.typeId in [13, 14]:
            if block['PlanetIDAndOwnerID']['OwnerID'] == 0:
                print PLANET_NAMES[block['PlanetIDAndOwnerID']['PlanetID']], block.typeId
                #print block['CurrentGravity']
                #print block['CurrentTemperature']
                #print block['CurrentRadiation']
                pprint(block.params)
                if 'Installations' in block.params:
                    p = block['Installations']
                    print 'Mines: %s Factories: %s' % (p['Mines'], p['Factories'])
        
        #if block.typeId == 7:
        #    print block.planets
        #    #print (bin(block.gameSettings)[2:] ).zfill(16)
            

    # Test race passwords and hashing
#     testRaceHash()

    pass


def testRaceHash():
    # The AI password and alternatives that show the weakness in the hash:
    print util.hashRacePassword("fymmgsd")
    print util.hashRacePassword("yfmmgsd")
    print util.hashRacePassword("iymtfi")
    print util.hashRacePassword("viewai")
    
    # This shows python's implicit integer overflow protection by returning a long integer :-/
    print util.hashRacePassword("aaaaaaaa")
    
    # Brute force the password
    util.guessRacePassword(util.read32([67, 18, 14, 0], 0), 5, 1, string.ascii_lowercase)

    # Current best found multiplayer AI password
    print util.hashRacePassword("TV+OdX+U")
    
    # Attempt to find a multiplayer AI password
#     util.guessRacePassword(4294967295, 5, 5, string.letters)
    

if __name__ == '__main__':
    main()