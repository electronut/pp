"""
makedata.py

Program to create test volumetric data sets.

Author: Mahesh Venkitachalam
"""

import sys, os
import numpy as np
import Image

def makeSphereCuboid():
    """create a volume with a sphere and a cuboid inside"""
    Nx, Ny, Nz = 256, 256, 256
    Nx2, Ny2, Nz2 = int(Nx/2), int(Ny/2), int(Nz/2)
    # fill with zeros
    a = np.zeros(Nx*Ny*Nz, np.uint8).reshape(Nx, Ny, Nz)
    # set data
    for k in range(Nz):
        for j in range(Ny):
            for i in range(Nx):
                # inside cuboid?
                if abs(i-Nx2) < 40 and abs(j-Ny2) < 30 and abs(k-Nz2) < 20:
                    a[i][j][k] = min(2*(-Nx2 + 40 + i), 255)
                else:
                    # inside sphere?
                    if ((i-Nx2)*(i-Nx2) + (j-Ny2)*(j-Ny2) + 
                        (k-Nz2)*(k-Nz2)) < 100*100:
                        a[i][j][k] = 50
    # create dir if not exists                
    imgDir = 'sphere-cuboid'
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    # write images
    for i in range(Nz):
        # create image from data
        im = Image.fromarray(a[i])
        # save file
        fileName = os.path.join(imgDir, 'sphere-cuboid%03d.png' % i)
        im.save(fileName)

# main() function
def main():
  # use sys.argv if needed
  print('running makedata...')
  makeSphereCuboid()

# call main
if __name__ == '__main__':
  main()
