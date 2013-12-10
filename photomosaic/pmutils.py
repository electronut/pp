################################################################################
# pmutils.py
#
# Author: Mahesh Venkitachalam
# Created:
#
# Description:
# 
# utility methods for photomosaic program
#
################################################################################

import sys, os, random, argparse
import Image
import imghdr
import numpy as np

def getAverageRGB(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # no. of pixels in image
  npixels = image.size[0]*image.size[1]
  # get colors as [(cnt1, (r1, g1, b1)), ...]
  cols = image.getcolors(npixels)
  # get [(c1*r1, c1*g1, c1*g2),...]
  sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols] 
  # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
  # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
  avg = tuple([sum(x)/npixels for x in zip(*sumRGB)])
  return avg

def getAverageRGBNP(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # get image as numpy array
  im = np.array(image)
  # get shape
  w,h,d = im.shape
  # change shape
  im.shape = (w*h, d)
  # get average
  return tuple(np.average(im, axis=0))

def splitImage(image, size):
  """
  Given Image and dims (rows, cols) returns an m*n list of Images 
  """
  W, H = image.size[0], image.size[1]
  m, n = size
  w, h = W/n, H/m
  # image list
  imgs = []
  # generate list of dimensions
  for j in range(m):
    row = []
    for i in range(n):
      # append cropped image
      imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
  return imgs

def getImages(image_dir):
  """
  given a directory of images, return a list of Images
  """
  files = os.listdir(image_dir)
  images = []
  for file in files:
    file_path = os.path.abspath(os.path.join(image_dir, file))
    try:
      # explicit load so we don't run into resource crunch
      fp = open(file_path, "rb")
      im = Image.open(fp)
      images.append(im)
      im.load() # force loading of the first frame
      fp.close() # force-close the file
    except:
      # skip
      print 'Invalid image: ', file_path
  return images

def getImageFilenames(image_dir):
  """
  given a directory of images, return a list of Image file names
  """
  files = os.listdir(image_dir)
  filenames = []
  for file in files:
    file_path = os.path.abspath(os.path.join(image_dir, file))
    try:
      imgType = imghdr.what(file_path) 
      if imgType:
        filenames.append(file_path)
    except:
      # skip
      print 'Invalid image: ', file_path
  return filenames

def getBestMatchIndex(input_avg, avgs):
  """
  return index of best Image match based on RGB value distance
  """

  # input image average
  avg = input_avg
  
  # get the closest RGB value to input, based on x/y/z distance
  index = 0
  min_index = 0
  min_dist = float("inf")
  for val in avgs:
    dist = ((val[0] - avg[0])*(val[0] - avg[0]) +
            (val[1] - avg[1])*(val[1] - avg[1]) +
            (val[2] - avg[2])*(val[2] - avg[2]))
    if dist < min_dist:
      min_dist = dist
      min_index = index
    index += 1

  return min_index


def createImageGrid(images, dims, gap = 0):
  """
  Given a list of images and a grid size (m, n), create 
  a grid of images. gap is the space between the tiles.
  """
  m, n = dims

  # sanity check
  assert m*n == len(images)

  # get max height and width of images
  # ie, not assuming they are all equal
  width = sorted([img.size[0] for img in images], reverse=True)[0]
  height = sorted([img.size[1] for img in images], reverse=True)[0]

  # create output image
  grid_img = Image.new('RGB', (n*(width + gap) + gap, m*(height + gap) + gap))
  
  # paste images
  for index in range(len(images)):
    row = index/n
    col = index - n*row
    grid_img.paste(images[index], (col*width, row*height))
    
  return grid_img

