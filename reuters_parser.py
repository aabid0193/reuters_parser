

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


class Artcl:
  
  def __init__(self, ts, authors, title, href, text):
    self.ts = ts
    self.authors = authors
    self.title = title
    self.href = href
    self.text = text


def csv_writer(artcl):
  '''
  '''
  pass


def json_writer(artcl):
  '''
  '''
  pass  


def parse_article(url):
  '''
  Responsible for parsing a single article.
  '''
  article = Article(url)

  print("url: {}".format(url))

  article.download()

  try:
    article.parse()
  except newspaper.article.ArticleException:
    print("Oops! The URL '{}' seems inaccessible!".format(url))

    article.authors = ['<UNK>']
    article.text = '<UNK>'

    return article

  return article

def clear_string(text):
  for c in rm_tokens:
    text = text.replace(c, '')

  return text

def generate_data(args):
  '''
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
        # Prepare the data?
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

  
  if csv_file is not None:
    csv_file.close()
  if json_file is not None:
    json_file.close()

  '''
  for filename in iglob(data_dir + '/*.pkl'):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                for datum in data:

                    ts = datum['ts']
                    if ts is None:
                        ts = ''

                    line = str(count)
                    line += sep
                    line += '"' + ts + '"'
                    line += sep
                    line += '"' + datum['title'] + '"'
                    line += sep
                    line += '"' + datum['href'] + '"'
                    line += '\n'

                    w.write(line)
                    print(count)
                    count += 1

  '''

def main():
  '''
  '''

  argparser = argparse.ArgumentParser(

  )
  argparser.add_argument(
    '--input_dir',
    type=str,
    help='The input directory'
  )
  argparser.add_argument(
    '--output_dir',
    type=str,
    help='The input directory'
  )
  argparser.add_argument(
    '-csv',
    action='store_true',
    help="Save data in csv file"
  )
  argparser.add_argument(
    '-json',
    action='store_true',
    help='Save data as json file'
  )
  argparser.add_argument(
    '-author',
    action='store_true',
    help='Store the author.'
  )
  argparser.add_argument(
    '-title',
    action='store_true',
    help='Store the title.'
  )
  argparser.add_argument(
    '-text',
    action='store_true',
    help='Store the text.'
  )

  args = argparser.parse_args()

  generate_data(args)


if __name__ == '__main__':
  main()
