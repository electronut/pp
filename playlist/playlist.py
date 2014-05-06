################################################################################
# playlist.py
#
# Author: Mahesh Venkitachalam
# 
# Purpose: Prints out common albums from 2 iTunes Playlists 
################################################################################

import re
import sys

def findUniqueAlbums(str):
    """given the XML playlist as string, returns a set of unique albums 
    """
    uniqAlbums = set(re.findall(r'<key>Album</key><string>(.+)</string>', str))
    return uniqAlbums

# Gather our code in a main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    nargs = len(sys.argv)
    if nargs == 2:
        # open file
        f = open(sys.argv[1])
        # read contents
        str = f.read()
        # get set of unique albums
        albums = findUniqueAlbums(str)
        # print out 
        print 'unique albums:', len(albums)
        for album in albums:
            print album
    elif nargs > 2:
        albumSets = []
        for arg in sys.argv[1:]:
            try:
                f = open(arg)
                # read contents
                # get set of unique albums
                albumSets.append(findUniqueAlbums(f.read()))
            except:
                print 'Error: could not open', arg
        # get common albums
        common = set.intersection(*albumSets)
        print 'common albums:', len(common)
        for album in common:
            print album

    else:
        print 'usage:\n'
        print 'To list album names:'
        print 'python playlist.py a.xml\n'
        print 'To find common albums:'
        print 'python playlist.py a.xml b.xml\n'
        

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
