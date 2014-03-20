"""
ascii.py

A python program that convert images to ASCII art.

Author: Mahesh Venkitachalam
"""

import sys, random, argparse
import numpy as np

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

def covertImageToAscii(fileName, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]
    w = int(W/cols)
    h = int(w/scale)
    rows = int(H/h)
    # ascii image is a list of strings
    aimg = []
    print("cols: %d, rows: %d" % (cols, rows))
    # generate list of dimensions
    for j in range(rows):
      aimg.append("")
      for i in range(cols):
          # append cropped image
          img = image.crop((i*w, j*h, (i+1)*w, (j+1)*h))
          avg = int(getAverageL(img))
          if moreLevels:
              gsval = gsmap1[avg]
          else:
              gsval = gsmap2[avg]
          aimg[j] += gsval
    # return txt
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
  aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels)

  # open file
  f = open(outFile, 'w')
    # write to file
  for k in range(len(aimg)):
      print(aimg[k], file=f)
  # cleancup
  f.close()

  print("done.")

# call main
if __name__ == '__main__':
  main()
