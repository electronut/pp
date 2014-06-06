
"""
playlist.py

Description: Prints out common albums from 2 iTunes Playlists 

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import re, argparse
import sys

def findUniqueAlbums(str):
    """given the XML playlist as string, returns a set of unique albums 
    """
    uniqAlbums = set(re.findall(r'<key>Album</key><string>(.+)</string>', str))
    return uniqAlbums

# Gather our code in a main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description="Comparing iTunes playlists...")
    # add expected arguments
    parser.add_argument('--common', nargs = '*', dest='plFiles', required=True)

    # parse args
    args = parser.parse_args()

    albumSets = []
    for arg in args.plFiles:
        try:
            f = open(arg)
            # read contents
            # get set of unique albums
            albumSets.append(findUniqueAlbums(f.read()))
        except:
            print('Error: could not open', arg)
    # get common albums
    common = set.intersection(*albumSets)
    print('common albums:', len(common))
    for album in common:
        print(album)

        

# main method
if __name__ == '__main__':
    main()
