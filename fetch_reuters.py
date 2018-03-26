# -*- coding: utf-8 -*-
'''
Copyright 2018, University of Freiburg.
Chair of Algorithms and Data Structures.
Markus Näther <naetherm@informatik.uni-freiburg.de>
'''

import os
import pickle
import argparse

from datetime import timedelta, date, datetime

import bs4
import requests


def get_soup_from_link(link):
  '''
  Parse an incoming link.
  '''
  if not link.startswith('http://www.reuters.com'):
    link = 'http://www.reuters.com' + link
  print(link)
  response = requests.get(link)
  assert response.status_code == 200
  return bs4.BeautifulSoup(response.content, 'html.parser')


def get_date_range(start_date, end_date):
  '''
  '''
  for i in range(int((end_date - start_date).days)):
    yield start_date + timedelta(i)

def fetch_reuters(args):
  today = datetime.now()
  output_dir = os.path.join(args.output_dir, 'output_' + today.strftime('%Y-%m-%d-%HH%MM'))

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  print('Generating the Full dataset in : {}'.format(output_dir))
  start_date = date(2007, 1, 1)
  end_date = today.date()
  iterations = 0
  for single_date in get_date_range(start_date, end_date):
    output = []
    string_date = single_date.strftime("%Y%m%d")
    link = 'http://www.reuters.com/resources/archive/us/{}.html'.format(string_date)
    # Small fallback to skip 
    try:
      soup = get_soup_from_link(link)
      targets = soup.find_all('div', {'class': 'headlineMed'})
    except Exception:
      print('Could not download link : {}. Resuming anyway.'.format(link))
      targets = []
    for target in targets:
      try:
        timestamp = str(string_date) + str(target.contents[1])
      except Exception:
        timestamp = None
        print('Timestamp set to None.')
      title = str(target.contents[0].contents[0])
      href = str(target.contents[0].attrs['href'])
      print('\tIterations = {}, date = {}, ts = {}, t = {}, h= {}'.format(str(iterations).zfill(9), string_date, timestamp, title, href))
      output.append({'ts': timestamp, 'title': title, 'href': href})
      iterations += 1

    output_filename = os.path.join(output_dir, string_date + '.pkl').format(output_dir, string_date)
    with open(output_filename, 'wb') as w:
      pickle.dump(output, w)
    print('>> Wrote dump to {}'.format(output_filename))
  

def main():
  '''
  Main routine.
  '''
  parser = argparse.ArgumentParser()

  # Output path
  parser.add_argument(
    '--output_dir',
    type=str, 
    help='The output directory where the downloaded and packed archives are saved.'
  )

  args = parser.parse_args()

  fetch_reuters(args)

if __name__ == '__main__':
  main()
