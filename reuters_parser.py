# -*- coding: utf-8 -*-
'''
Copyright 2018, University of Freiburg.
Chair of Algorithms and Data Structures.
Markus Näther <naetherm@informatik.uni-freiburg.de>
'''

import os, sys
import argparse
import ijson
import csv
import bs4
import requests
import pickle
from glob import iglob

from datetime import timedelta, date, datetime

from newspaper import Article
import newspaper

rm_tokens = ['\n', '\t', '\r']


class Artcl(object):
  '''
  Artcl is the description of a single article. In general every article from every
  news/article page can be used here.
  '''
  
  def __init__(self, ts, authors, title, href, text):
    '''
    Constructor.
    '''
    self.ts = ts
    self.authors = authors
    self.title = title
    self.href = href
    self.text = text

def parse_article(url):
  '''
  Responsible for parsing a single article.
  '''
  article = Article(url)

  print("Download data of URL: {}".format(url))

  article.download()

  # Fallback, otherwise the program would exit on the first invalid URL
  try:
    article.parse()
  except newspaper.article.ArticleException:
    print("Oops! The URL '{}' seems inaccessible!".format(url))

    article.authors = ['<UNK>']
    article.text = '<UNK>'

    return article

  return article

def clear_string(text):
  '''
  Cleanup the incoming string, thereby every character of rm_tokens will be removed.
  '''
  for c in rm_tokens:
    text = text.replace(c, '')

  return text

def generate_data(args):
  '''
  The final method for generating the data output files.

  The code should be self explanatory.
  '''
  in_dir = args.input_dir
  out_dir = args.output_dir

  csv_file = None
  json_file = None
  if args.csv:
    csv_file = open(out_dir + '/output.csv', 'w')
  if args.json:
    json_file = open(out_dir + '/output.json', 'w')

  for filename in iglob(in_dir + '/*.pkl'):
    with open(filename, 'rb') as fin:
      data = pickle.load(fin)

      if json_file:
        json_file.write("[\n")
    
      for item in data:
        
        aux_author = ""
        aux_text = ""
        # Prepare the data, for the text and the authors some extra work have to be done
        if args.author or args.text:
          artcl = parse_article(item['href'])

          aux_author = ', '.join(a for a in artcl.authors)
          aux_text = clear_string(artcl.text)

        if args.csv:
          ts = item['ts']
          if ts is None:
            ts = ''
          line = '"' + ts + '"'
          line += '\t'
          if args.title:
            line += '"' + item['title'] + '"'
            line += '\t'
          if args.author:
            line += '"' + aux_author + '"'
            line += '\t'
          if args.text:
            line += '"' + aux_text + '"'
            line += '\t'
          line += '\n'
          csv_file.write(line)

        if args.json:
          ts = item['ts']
          if ts is None:
            ts = ''
          line = '{ ts: "' + ts + '", '
          if args.title:
            line += 'title: "' + item['title'] + '", '
          if args.author:
            line += 'authors: "' + aux_author + '", '
          if args.text:
            line += 'text: "' + aux_text + '" }'
          line += ',\n'
          json_file.write(line)
      
  if json_file:
    json_file.write("\n]")  

  # Close the files
  if csv_file:
    csv_file.close()
  if json_file:
    json_file.close()

def main():
  '''
  Main routine.
  '''

  argparser = argparse.ArgumentParser()
  argparser.add_argument(
    '--input_dir',
    type=str,
    help='The input directory'
  )
  argparser.add_argument(
    '--output_dir',
    type=str,
    help='The output directory'
  )
  argparser.add_argument(
    '-csv',
    action='store_true',
    help="Save all parsed data within an csv file"
  )
  argparser.add_argument(
    '-json',
    action='store_true',
    help='Save all parsed data within an json file'
  )
  argparser.add_argument(
    '-author',
    action='store_true',
    help='Store the author information.'
  )
  argparser.add_argument(
    '-title',
    action='store_true',
    help='Store the title information.'
  )
  argparser.add_argument(
    '-text',
    action='store_true',
    help='Store the text information.'
  )

  args = argparser.parse_args()

  generate_data(args)


if __name__ == '__main__':
  main()
