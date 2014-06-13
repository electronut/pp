
"""
playlist.py

Description: Prints out common albums from 2 iTunes Playlists 

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np

def plotStats(fileName):
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks
    tracks = plist['Tracks']
    # create a track-length dict
    trackLen = {}
    # iterate through tracks
    for k, v in tracks.items():
        try:
            trackLen[v['Name']] = v['Total Time']
        except:
            print("Error", k, v)
    #print(trackLen)

    # plot
    x = np.arange(len(trackLen))
    y = np.array(list(trackLen.values()), np.int32)
    pyplot.plot(x, y, 'o')
    pyplot.show()


def findDuplicates(fileName):
    """
    Find duplicate tracks in given playlist.
    """
    print('Finding duplicate tracks in %s...' % fileName)
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks
    tracks = plist['Tracks']
    # create a track name dict
    trackNames = {}
    # iterate through tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # is there an entry already?
            if name in trackNames:
                # if name and duration matches, increment count
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add entry - duration and count
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass
    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save dups to file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        prints("No duplicate tracks found!")
    f = open("dups.txt", 'w')
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()

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
    parser.add_argument('--common', nargs = '*', dest='plFiles', required=False)
    parser.add_argument('--stats', dest='plFile', required=False)
    parser.add_argument('--dup', dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
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
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    else:
        findDuplicates(args.plFileD)
        
    # find duplicate tracks

# main method
if __name__ == '__main__':
    main()
