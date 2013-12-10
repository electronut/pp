################################################################################
# photomosaic.py
#
# Author: Mahesh Venkitachalam
# Created:
#
# Description:
# 
# Creates a photomosaic given a target image and a folder of input images
#
################################################################################

import sys, os, random, argparse
import Image
from pmutils import *

def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images=True, gap = 0):
  """
  Creates photomosaic given target and input images.
  """

  print 'splitting input image...'
  # split target image 
  target_images = splitImage(target_image, grid_size)

  print 'finding image matches...'
  # for each target image, pick one from input
  output_images = []
  # for user feedback
  count = 0
  batch_size = len(target_images)/10

  # calculate input image averages
  avgs = []
  for img in input_images:
    avgs.append(getAverageRGB(img))

  for img in target_images:
    # target sub-image average
    avg = getAverageRGB(img)
    # find match index
    match_index = getBestMatchIndex(avg, avgs)
    output_images.append(input_images[match_index])
    # user feedback
    if count > 0 and count % batch_size is 0:
      print 'processed ' + str(count) + ' of ' + str(len(target_images)) + '...' 
    count += 1
    # remove selected image from input if flag set
    if not reuse_images:
      input_images.remove(match)

  print 'creating mosaic...'
  # draw mosaic to image
  mosaic_image = createImageGrid(output_images, grid_size, gap)

  # return mosaic
  return mosaic_image

# Gather our code in a main() function
def main():
  # Command line args are in sys.argv[1], sys.argv[2] ..
  # sys.argv[0] is the script name itself and can be ignored

  # parse arguments
  parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
  # add arguments
  parser.add_argument('--target-image', dest='target_image', required=True)
  parser.add_argument('--input-folder', dest='input_folder', required=True)
  parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
  parser.add_argument('--output-file', dest='outfile', required=False)

  args = parser.parse_args()

  ###### INPUTS ######

  # target image
  target_image = Image.open(args.target_image)

  # input images
  print 'reading input folder...'
  input_images = getImages(args.input_folder)

  # shuffle list - to get a more varied output?
  random.shuffle(input_images)

  # size of grid
  grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

  # output
  output_filename = 'mosaic.png'
  if args.outfile:
    output_filename = args.outfile
  
  # re-use any image in input
  reuse_images = True

  #gap between images
  gap = 0

  # resize the input to fit original image size?
  resize_input = True

  ##### END INPUTS #####

  print 'starting photomosaic creation...'
  
  # if images can't be reused, ensure m*n <= num_of_images 
  if not reuse_images:
    if grid_size[0]*grid_size[1] > len(input_images):
      print 'grid size less than number of images'
      exit()
  
  # resizing input
  if resize_input:
    print 'resizing images...'
    # for given grid size, compute max dims w,h of tiles
    dims = (target_image.size[0]/grid_size[1], 
            target_image.size[1]/grid_size[0]) 
    print 'max tile dims: ', dims
    # resize
    for img in input_images:
      img.thumbnail(dims)

  # create photomosaic
  mosaic_image = createPhotomosaic(target_image, input_images, grid_size,
                                   reuse_images, gap)

  # write out mosaic
  mosaic_image.save(output_filename, 'PNG')

  print 'saved output to', output_filename
  print 'done.'

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
