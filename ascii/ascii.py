"""
ascii.py

A python program that convert images to ASCII art.

Author: Mahesh Venkitachalam
"""

import argparse
import numpy as np
import math

from PIL import Image

# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = '@%#*+=-:. '

def covertImageToAscii(fileName, cols=80, scale=0.43, moreLevels=False):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals
    global gscale1, gscale2
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
    # store dimensions
    W, H = image.size
    print("input image dims: %d x %d" % (W, H))
    # compute width of tile
    w = W//cols
    # compute tile height based on aspect ratio and scale
    h = int(w/scale)
    # compute number of rows
    rows = int(H / h)
    
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        raise Exception("Image too small for specified cols!")

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = j*h
        y2 = (j+1)*h
        # correct last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop image to tile
            x1 = i*w
            x2 = (i+1)*w
            # correct last tile
            if i == cols-1:
                x2 = W
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
            # get average luminance
            avg = int(np.average(img))
            # look up ascii char
            if moreLevels:
                gsval = gscale1[(avg*69)//255]
            else:
                gsval = gscale2[(avg*9)//255]
            # append ascii char to string
            aimg[j] += gsval
    
    # return txt image
    return aimg

# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(
        description="This program converts an image into ASCII art.")
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', default=0.43, type=float)
    parser.add_argument('--out', dest='outFile', default='out.txt')
    parser.add_argument('--cols', dest='cols', default=80, type=int)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    # parse args
    args = parser.parse_args()

    # set output file
    outFile = args.outFile
    # set scale default as 0.43 which suits a Courier font
    scale = args.scale
    # set cols
    cols = args.cols

    print('generating ASCII art...')
    # convert image to ascii txt
    aimg = covertImageToAscii(args.imgFile, cols, scale, args.moreLevels)

    # open file
    with open(outFile, 'w') as f:
        # write to file
        f.write('\n'.join(aimg))

    print("ASCII art written to %s" % outFile)

# call main
if __name__ == '__main__':
    main()
