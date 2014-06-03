"""
spiro.py

A python program that simulates a Sprirograph.

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, random, argparse
import numpy as np
import math


# main() function
def main():
  # use sys.argv if needed
  print('generating spirograph...')
  # create parser
  parser = argparse.ArgumentParser(description="Sprirograph...")
  """
  # add expected arguments
  parser.add_argument('--file', dest='imgFile', required=True)
  parser.add_argument('--scale', dest='scale', required=False)
  parser.add_argument('--out', dest='outFile', required=False)
  parser.add_argument('--cols', dest='cols', required=False)
  parser.add_argument('--morelevels',dest='moreLevels',action='store_true')
  """

  # parse args
  # args = parser.parse_args()
  

# call main
if __name__ == '__main__':
  main()
