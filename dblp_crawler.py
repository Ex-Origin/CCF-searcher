#!/usr/bin/python3

import requests
import re
import time
import html
import urllib
import json
import os
import logging
import csv
import traceback
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
output_csv = open('dblp_crawler_output.csv', 'w')
output_csv.write('year,title,doi-url,authors,ccf-rank,abbreviation,ccf-name,full-name,publisher\n')

def requests_and_parse(url:str) -> BeautifulSoup:
    '''
    Instantiate a BeautifulSoup class by providing a URL.
    '''

    i = 0
    raw_response = False
    status_code = 0
    while(i < 5 and (not raw_response) and status_code != 404):
        i += 1
        try:
            raw_response = requests.get(url, timeout=10)
            status_code = raw_response.status_code

            if(status_code == 404):
                pass
            elif(status_code == 200):
                pass
            elif(status_code == 503):
                logging.warning(f'HTTP {raw_response.status_code} at {url}')
                time.sleep(60)
            else:
                logging.warning(f'HTTP {raw_response.status_code} at {url}')

        except Exception as e:
            logging.error(f'{str(e)} at {url}')
            status_code = 0
            time.sleep(60)

    if(raw_response and raw_response.status_code == 200):
        return BeautifulSoup(raw_response.text, 'html.parser')
    else:
        logging.warning(f'The request to {url} has failed. {str(raw_response)}')
        return None

def csv_unquote(s):
    '''
    Transform the input string into a single CSV element.
    '''
    s = s.replace('"', '""')
    if(s.find(',') != -1 or s.find(';') != -1):
        s = '"' + s + '"'
    return s

def dblp_journals(journal_item, url):
    '''
    Retrieve the information from the journal publications.
    '''
    soup = requests_and_parse(url)
    if(not soup):
        return
    
    tmp = soup.select("div#main > header > h2")
    if(tmp):
        tmp2 = re.findall('[12]\d\d\d', tmp[0].get_text())
        if(tmp2):
            year = tmp2[0]
        else:
            logging.warning(f'Not found year in "{url}", ignore it.')
            return
    else:
        logging.warning(f'The select("div#main > header > h2") is not present in "{url}", ignore it.')
        return
    
    article_item = soup.select("div#main > ul.publ-list > li.article")
    full_name = soup.select("header#headline > h1")[0].get_text().replace('\n', '')
    for article in article_item:
        title = article.select("span.title")[0].get_text()
        doi_url = ''
        tmp = article.select("li.drop-down:first-child > div.head > a")
        if(tmp):
            doi_url = tmp[0]['href']
        authors = ','.join([author.get_text() for author in article.select('span[itemprop="author"] > a > span[itemprop="name"]')])
        data_item = ','.join([
            csv_unquote(year),
            csv_unquote(title),
            csv_unquote(doi_url),
            csv_unquote(authors),
            csv_unquote(journal_item['ccf-rank']),
            csv_unquote(journal_item['abbreviation']),
            csv_unquote(journal_item['ccf-name']),
            csv_unquote(full_name),
            csv_unquote(journal_item['publisher']),
        ])
        output_csv.write(data_item + '\n')

def dblp_journals_handler(journal_item:dict) -> None:
    '''
    Retrieve the sub-page
    '''
    soup = requests_and_parse(journal_item['url'])
    if(soup):
        child_item = soup.select('div#main > ul > li > a')
        if(child_item):
            for item in child_item:
                logging.debug(f'dblp_journals("{item["href"]}")')
                dblp_journals(journal_item, item['href'])
        else:
            logging.error(f'The select("div#main > ul > li > a") is not present in {journal_item["url"]}')

def dblp_conf(conf_item, url):
    '''
    Retrieve the information from the conference publications.
    '''
    soup = requests_and_parse(url)
    if(not soup):
        return
    inproceedings_item = soup.select("div#main > ul.publ-list > li.inproceedings")

    full_name = ''
    tmp = soup.select("li.editor span.title")
    if(tmp):
        full_name = tmp[0].get_text().replace('\n', '')

    year = '-1'
    tmp = soup.select('li.editor span[itemprop="datePublished"]')
    if(tmp):
        year = tmp[0].get_text()

    for inproceeding in inproceedings_item:
        title = inproceeding.select("span.title")[0].get_text()
        doi_url = ''
        tmp = inproceeding.select("li.drop-down:first-child > div.head > a")
        if(tmp):
            doi_url = tmp[0]['href']
        authors = ','.join([author.get_text() for author in inproceeding.select('span[itemprop="author"] > a > span[itemprop="name"]')])
        data_item = ','.join([
            csv_unquote(year),
            csv_unquote(title),
            csv_unquote(doi_url),
            csv_unquote(authors),
            csv_unquote(conf_item['ccf-rank']),
            csv_unquote(conf_item['abbreviation']),
            csv_unquote(conf_item['ccf-name']),
            csv_unquote(full_name),
            csv_unquote(conf_item['publisher']),
        ])
        output_csv.write(data_item + '\n')

def dblp_conf_handler(conf_item:dict) -> None:
    '''
    Retrieve the sub-page
    '''
    soup = requests_and_parse(conf_item['url'])
    if(soup):
        child_item = soup.select('ul.publ-list li.drop-down:first-child > div.head > a')
        if(child_item):
            for item in child_item:
                logging.debug(f'dblp_conf("{item["href"]}")')
                dblp_conf(conf_item, item['href'])
        else:
            logging.error(f'The select("ul.publ-list li.drop-down:first-child > div.head > a") is not present in {conf_item["url"]}')

if __name__ == '__main__':
    dblp_journals_patterns = re.compile('^https{0,1}://dblp.uni-trier.de/db/journals/')
    dblp_conf_patterns = re.compile('^https{0,1}://dblp.uni-trier.de/db/conf/')
    ccf_data = list(csv.DictReader(open('CCF_rank_2022.csv', 'r')))
    for i in range(len(ccf_data)):
        logging.info('%03d/%03d - %s' % (i+1, len(ccf_data), ccf_data[i]['url']))
        if(dblp_journals_patterns.match(ccf_data[i]['url'])):
            dblp_journals_handler(ccf_data[i])
        elif(dblp_conf_patterns.match(ccf_data[i]['url'])):
            dblp_conf_handler(ccf_data[i])
        else:
            logging.warning(f'Unsupported url {ccf_data[i]["url"]}')
    logging.info('END')
