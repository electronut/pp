################################################################################
# modern.py
#
# Author: Mahesh Venkitachalam
# Created: Oct 2012
#
# Description: Create a nicely formatted 2-sided page of Modern Library's 
#              100 best book list. Generated LaTeX file that can be used 
#              to create a PDF.
#
################################################################################

import sys, re, urllib
from bs4 import BeautifulSoup
import unicodedata

# header for latex file
strLatexHeader = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[margin=0.2in]{geometry}
\usepackage{array}
\usepackage{color}
\usepackage{url}
\usepackage[usenames,table,dvipsnames]{xcolor}
\newcommand{\bookentry}[3]{%
    \parbox{0.25in}{\textcolor{gray}{\textbf{#1}}}~\parbox{1.35in}{\tiny\textsc{#2} \\ \textbf{#3}}
}
\begin{document}
"""

# footer for latex file
strLatexFooter = r"""
\end{document}
"""

# create a .tex LaTeX file formatted with book data
def createLatexFile(bookLists, filename):
  # expecting only 2 entries
  assert len(bookLists) == 2
  assert len(bookLists[0]) == 2
  assert len(bookLists[1]) == 2

  # open output file
  f = open(filename, 'w')
  # header
  f.write(strLatexHeader)
  # page 1
  writePage(f, bookLists[0], 'novels')
  # page 2
  f.write(r'\newpage' + '\n')
  writePage(f, bookLists[1], 'non-fiction')

  # footer
  f.write(strLatexFooter)
  # close file
  f.close()

# generate LaTeX code for 1 page
def writePage(f, bookList, caption):
  f.write(r'\noindent {\small \textsc{modern library 100 best %s}} \\' % 
          caption)
  if caption is 'novels':
    f.write(r'\url{http://www.modernlibrary.com/top-100/100-best-novels/} \\ \\')
  else:
    f.write(r'\url{http://www.modernlibrary.com/top-100/100-best-nonfiction/} \\ \\')

  # list
  f.write(r'\begin{tabular}{cc}')
  f.write(r'\textsc{board} & \textsc{reader} \\')

  # for each section (board/reader)
  for secnum,section in enumerate(bookList):
    f.write(r'\begin{tabular}{ll}') 
    f.write(r'\arrayrulecolor{gray}\hline')
    for index, item in enumerate(section[:50]):
      b1 = item
      b2 = section[50 + index]
    #print item
      f.write(r"""
\bookentry{%d}{%s}{%s} & \bookentry{%d}{%s}{%s} \\ \arrayrulecolor{gray}\hline
""" % (b1[0], b1[1], b1[2], b2[0], b2[1], b2[2]))
      
    f.write(r'\end{tabular}')
    if secnum == 0:
      f.write(r'&')
  # end main tabular
  f.write(r'\end{tabular}')

# returns a list [L1, L2] where L1 & L2 are of the form 
# [(#, book, author),...]
def getBookList(strHTML):
  # create list
  bookList = []
  # load html
  soup = BeautifulSoup(strHTML)
  # find all relavent divs
  divTags = soup.find_all('div', 'list-100')
  # we expect only two
  assert len(divTags) == 2
  # for each div/list-100
  for divTag in divTags:
    list1 = []
    # find all list elements
    liTags = divTag.find_all('li')
    for index, liTag in enumerate(liTags):
      match = re.findall(r'(.+)by(.+)', liTag.text)
      # expect only 1 match eg.: [('a', 'b')]
      assert len(match) == 1
      # add to list
      list1.append((index+1, 
                    match[0][0].encode('ascii','ignore').strip(), 
                    match[0][1].encode('ascii','ignore').strip()))
    # add to main list
    bookList.append(list1)
  # return book list
  return bookList

# find common titles from the 2 sub-lists in the booklist
def findCommonTitles(bookList):
  # check if there are 2 sub-lists
  assert len(bookList) is 2
  # gather (title, author) pairs
  s1 = set([(x[1], x[2]) for x in bookList[0]])
  s2 = set([(x[1], x[2]) for x in bookList[1]])
  # common items
  common = list(set.intersection(s1, s2))
  # return list 
  return common

# main() function
def main():
  # use sys.argv if needed
  print 'reading novel list...'
  strHTML1 = urllib.urlopen(r'http://www.randomhouse.com/modernlibrary/100bestnovels.html').read()
  bl1 = getBookList(strHTML1)
  print 'reading non-fiction list...'
  strHTML2 = urllib.urlopen(r'http://www.modernlibrary.com/top-100/100-best-nonfiction/').read()
  bl2 = getBookList(strHTML2)
  # create master list
  BL = [bl1, bl2]
  # create latex file
  createLatexFile(BL, 'modern-list.tex')
  print 'created LaTeX file modern-list.tex. Run \'pdflatex modern-list.tex\' to generate PDF.'
  # save common novels to file
  print 'writing common novels to common-novels.txt...'
  f = open('common-novels.txt', 'w')
  commonNovels = findCommonTitles(bl1)
  for entry in commonNovels:
    f.write(entry[0] + ' by ' + entry[1] + '\n')
  f.close()
  # save nonfiction to file
  print 'writing common nonfiction to common-nonfiction.txt...'
  f = open('common-nonfiction.txt', 'w')
  commonNF = findCommonTitles(bl2)
  for entry in commonNF:
    f.write(entry[0] + ' by ' + entry[1] + '\n')
  f.close()

# call main
if __name__ == '__main__':
  main()
