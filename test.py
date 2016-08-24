'''
Created on Jul 19, 2014

@author: raptor
'''
from blocks import BLOCKS, PLANET_NAMES
from encryption import decryptor
import sys
from pprint import pprint


def main():
    starsFile = sys.argv[1]
    # Retrieve a list of decrypted blocks from the file
    blocks = decryptor.readFile(starsFile)
    
    # Now do great and amazing things with the blocks!
    planet_block = None
    for block in blocks:
        if block.typeId not in BLOCKS:
            print 'Unknown block:', block.typeId
            continue
        #print BLOCKS[block.typeId], block.typeId
        if block.typeId in [13, 14]:
            if block['PlanetIDAndOwnerID']['OwnerID'] == 0:
                print PLANET_NAMES[block['PlanetIDAndOwnerID']['PlanetID']], block.typeId
                pprint(block.params)
                if 'Installations' in block.params:
                    p = block['Installations']
                    print 'Mines: %s Factories: %s' % (p['Mines'], p['Factories'])
            pass


if __name__ == '__main__':
    main()