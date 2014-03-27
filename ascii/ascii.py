"""
ascii.py

A python program that convert images to ASCII art.

Author: Mahesh Venkitachalam
"""

import sys, random, argparse
import numpy as np
import math

from PIL import Image

# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
keys = range(256)
vals = [gscale1[int((v*69)/255)] for v in keys]
gsmap1 = dict(zip(keys, vals))

# 10 levels of gray
gscale2 = '@%#*+=-:. '
vals = [gscale2[int((v*9)/255)] for v in keys]
gsmap2 = dict(zip(keys, vals))

def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
    # get shape
    w,h = im.shape
    # get average
    return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, cols, scale, moreLevels, invert):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))
    # compute width of tile
    w = W/cols
    # compute tile height based on aspect ratio and scale
    h = int(w/scale)
    # compute number of rows
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
      # append an empty string
      aimg.append("")
      for i in range(cols):
          # crop image to tile
          x2 = int((i+1)*w)
          # correct last tile
          if i == cols-1:
              x2 = W
          img = image.crop((int(i*w), j*h, x2, (j+1)*h))
          # get average luminance
          avg = int(getAverageL(img))
          # invert if flag set
          if invert:
              avg = 255 - avg
          # look up ascii char
          if moreLevels:
              gsval = gscale1[int((avg*69)/255)]
          else:
              gsval = gscale2[int((avg*9)/255)]
          # append ascii char to string
          aimg[j] += gsval
    # return txt image
    return aimg

# main() function
def main():
  # use sys.argv if needed
  print('generating ASCII art...')
  # create parser
  parser = argparse.ArgumentParser(description="ASCI Art...")
  # add expected arguments
  parser.add_argument('--file', dest='imgFile', required=True)
  parser.add_argument('--scale', dest='scale', required=False)
  parser.add_argument('--out', dest='outFile', required=False)
  parser.add_argument('--cols', dest='cols', required=False)
  parser.add_argument('--invert', dest='invert', action='store_true')
  parser.add_argument('--morelevels',dest='moreLevels',action='store_true')

  # parse args
  args = parser.parse_args()
  
  imgFile = args.imgFile
  # set output file
  outFile = 'out.txt'
  if args.outFile:
      outFile = args.outFile
  # set scale
  scale = 0.43
  if args.scale:
      scale = float(args.scale)
  # set cols
  cols = 80
  if args.cols:
      cols = int(args.cols)

  # convert image to ascii txt
  aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels, args.invert)

  # open file
  f = open(outFile, 'w')
    # write to file
  for k in range(len(aimg)):
      print(aimg[k], file=f)
  # cleanup
  f.close()

  print("ASCII art written to %s" % outFile)

# call main
if __name__ == '__main__':
  main()
