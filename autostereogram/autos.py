"""
autos.py

Creating Autostereograms

Author: Mahesh Venkitachalam
"""

import sys, random, argparse
from PIL import Image, ImageDraw

# create spacing/depth example
def createSpacingDepthExample():
    tiles = [Image.open('test/a.png'), Image.open('test/b.png'), 
             Image.open('test/c.png')]
    img = Image.new('RGB', (600, 400), (0, 0, 0))
    spacing = [10, 20, 40]
    for j, tile in enumerate(tiles):
        for i in range(8):
            img.paste(tile, (10 + i*(100 + j*10), 10 + j*100))
    img.save('sdepth.png')

# create image filled with random dots
def createRandomTile(dims):
  # create image
  img = Image.new('RGB', dims)
  draw = ImageDraw.Draw(img)
  # calculate radius - % of min dimension 
  r = int(min(*dims)/100)
  # number of dots
  n = 1000
  # draw random circles
  for i in range(n):
    # -r is used so circle stays inside - cleaner for tiling
    x, y = random.randint(0, dims[0]-r), random.randint(0, dims[1]-r)
    fill = (random.randint(0, 255), random.randint(0, 255), 
            random.randint(0, 255))
    draw.ellipse((x-r, y-r, x+r, y+r), fill)
  # return image
  return img

# Create a larger image of size dims by tiling the given image
def createTiledImage(tile, dims):
  # create output image
  img = Image.new('RGB', dims)
  W, H = dims
  w, h = tile.size
  # calculate # of tiles needed
  cols = int(W/w) + 1
  rows = int(H/h) + 1
  # paste tiles
  for i in range(rows):
    for j in range(cols):
      img.paste(tile, (j*w, i*h))
  # output image
  return img

# create a depth map for testing:
def createDepthMap(dims):
  dmap = Image.new('L', dims)
  dmap.paste(10, (200, 25, 300, 125))
  dmap.paste(30, (200, 150, 300, 250))
  dmap.paste(20, (200, 275, 300, 375))
  return dmap

# Given a depth map (image) and an input image, create a new image
# with pixels shifted according to depth
def createDepthShiftedImage(dmap, img):
  # size check
  assert dmap.size == img.size
  # create shifted image
  sImg = img.copy()
  # get pixel access
  pixD = dmap.load()
  pixS = sImg.load()
  # shift pixels output based on depth map
  cols, rows = sImg.size
  for j in range(rows):
    for i in range(cols):
      xshift = pixD[i, j]/10
      xpos = i - 140 + xshift
      if xpos > 0 and xpos < cols:
        pixS[i, j] = pixS[xpos, j]
  # return shifted image
  return sImg

# Given a depth map (image) and an input image, create a new image
# with pixels shifted according to depth
def createAutostereogram(dmap, tile):
  # convert depth map to single channel if needed
  if dmap.mode is not 'L':
    dmap = dmap.convert('L')
  # if no tile specified, use random image
  if not tile:
    tile = createRandomTile((100, 100))
  # create an image by tiling
  img = createTiledImage(tile, dmap.size)
  # create shifted image
  sImg = img.copy()
  # get pixel access
  pixD = dmap.load()
  pixS = sImg.load()
  # shift pixels output based on depth map
  cols, rows = sImg.size
  for j in range(rows):
    for i in range(cols):
      xshift = pixD[i, j]/10
      xpos = i - tile.size[0] + xshift
      if xpos > 0 and xpos < cols:
        pixS[i, j] = pixS[xpos, j]
  # return shifted image
  return sImg

# main() function
def main():
  # use sys.argv if needed
  print('creating autostereogram...')
  # create parser
  parser = argparse.ArgumentParser(description="Autosterograms...")
  # add expected arguments
  parser.add_argument('--depth', dest='dmFile', required=True)
  parser.add_argument('--tile', dest='tileFile', required=False)
  parser.add_argument('--out', dest='outFile', required=False)
  # parse args
  args = parser.parse_args()
  # set output file
  outFile = 'as.png'
  if args.outFile:
      outFile = args.outFile
  # set tile
  tileFile = False
  if args.tileFile:
      tileFile = Image.open(args.tileFile)
  # open depth map
  dmImg = Image.open(args.dmFile)
  # create stereogram
  asImg = createAutostereogram(dmImg, tileFile)
  # write output
  asImg.save(outFile)

# call main
if __name__ == '__main__':
  main()
