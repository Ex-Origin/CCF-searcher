#!/usr/bin/python3

import requests
import re
import time
import html
import urllib
import json
import os
import cloudscraper
from urllib.parse import unquote

def out_print(info):
    print('[%s] : %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), info), flush=True)

def get(url):
    '''
    Return set 
    (real_url, text_without_line)
    '''
    i = 0
    raw_response = False
    status_code = 0
    while(i < 5 and (not raw_response) and status_code != 404):
        i += 1

        try:
            raw_response = session.get(url, proxies=proxy, timeout=10)
            status_code = raw_response.status_code

            if('xplore-shut-page.html' in raw_response.url):
                out_print('Warn: IEEE Xplore is temporarily unavailable')
                time.sleep(10)

            if(status_code == 404):
                pass
            elif(status_code == 200):
                pass
            elif(status_code == 503):
                out_print('Warn: HTTP %d at %s' % (raw_response.status_code, url))
                time.sleep(10)
            else:
                out_print('Warn: HTTP %d at %s' % (raw_response.status_code, url))

        except Exception as e:
            out_print(str(e))
            status_code = 0
            time.sleep(10)

    if(raw_response and raw_response.status_code == 200):
        return (raw_response.url, raw_response.text.replace('\n', ''))
    else:
        out_print('Error: ' + str(raw_response))
        return ('', '')

def usenix_handler(text_without_line):
    '''
    Return list 
    [abstract]
    '''
    abstract = ''

    head = text_without_line.find('Abstract:')
    tail = text_without_line.find('</div>', head + 21)
    if(head != -1 and tail != -1):
        tmp = re.findall('<p>(.+?)</p>', text_without_line[head + 21 : tail])
        if(tmp):
            tmp = '\n'.join(tmp)
            tmp = re.sub('<.+?>', '', tmp)
            tmp = html.unescape(tmp) 
            abstract = tmp
        else:
            out_print("Not found abstract.")
    else:
        out_print("Not found abstract.")

    return [abstract]

def acm_handler(text_without_line):
    '''
    Return list 
    [abstract]
    '''
    abstract = ''

    head = text_without_line.find('<div class="abstractSection abstractInFull">')
    tail = text_without_line.find('</div>', head + 1)
    if(head != -1 and tail != -1):
        tmp = re.findall('<p>(.+?)</p>', text_without_line[head + 21 : tail])
        if(tmp):
            tmp = '\n'.join(tmp)
            tmp = re.sub('<.+?>', '', tmp)
            tmp = html.unescape(tmp) 
            abstract = tmp
        else:
            out_print("Not found abstract.")
    else:
        out_print("Not found abstract.")

    return [abstract]

def ieee_handler(text_without_line):
    '''
    Return list 
    [abstract]
    '''
    abstract = ''

    head = text_without_line.find(',"abstract":"')
    tail = text_without_line.find('","', head + 13 )
    if(head != -1 and tail != -1):
        tmp = text_without_line[head + 13 :tail]\
            .replace('\\n', '\n').replace('\\\'', '\'').replace('\\\"', '\"').replace('\\\\', '\\')
        if(tmp):
            tmp = re.sub('<.+?>', '', tmp)
            tmp = html.unescape(tmp) 
            abstract = tmp
        else:
            out_print("Not found abstract.")
    else:
        out_print("Not found abstract.")

    return [abstract]

def elsevier_handler(text_without_line):
    '''
    Return list 
    [abstract]
    '''
    abstract = ''

    head = text_without_line.find('?Redirect=')
    if(head == -1):
        return [abstract]
    head += 10
    tail = text_without_line.find("'", head)
    url = unquote(text_without_line[head: tail])
    real_url, new_text_without_line = get(url)
    if('www.sciencedirect.com' not in real_url):
        out_print('Error: in elsevier_handler, %s -> %s' % (url, real_url))

    head = new_text_without_line.find('">Abstract</h2>')
    tail = new_text_without_line.find('</div>', head + 15)
    if(head != -1 and tail != -1):
        tmp = re.findall('<p.*?>(.+?)</p>', new_text_without_line[head + 15 : tail])
        if(tmp):
            tmp = '\n'.join(tmp)
            tmp = re.sub('<.+?>', '', tmp)
            tmp = html.unescape(tmp) 
            abstract = tmp
        else:
            out_print("Not found abstract.")
    else:
        out_print("Not found abstract.")
    
    return [abstract]

def main_handler(search_list, start=1):
    '''
    Return matrix 
    [[class, abbreviation, year, title, doi_url, authors, abstract], 
     [class, abbreviation, year, title, doi_url, authors, abstract]]
    '''
    length = len(search_list)
    num = length - (start - 1)
    paper_info = []
    for pi in range(num):
        instance_url = search_list[(start - 1) + pi][2] # DOI
        out_print('(%03d/%03d) Deal with: %s' % (start + pi, length, instance_url))

        result = get(instance_url)
        if(result):
            if('www.usenix.org' in result[0]):
                abstract = usenix_handler(result[1])
            elif('dl.acm.org' in result[0]):
                time.sleep(10)
                abstract = acm_handler(result[1])
            elif('ieeexplore.ieee.org' in result[0]):
                abstract = ieee_handler(result[1])
            elif('linkinghub.elsevier.com' in result[0]): # www.sciencedirect.com
                abstract = elsevier_handler(result[1])
            else:
                abstract = ['']
                out_print('Unknown pattern %s' % (result[0]))

            paper_info += [search_list[(start - 1) + pi] + abstract]  
    
    return paper_info



if(__name__ == '__main__'):
    search_list = [
        # [2021, "Self-Adaptive Sampling for Network Traffic Measurement", "https://doi.org/10.1109/INFOCOM42981.2021.9488425", "", "CCF-A", "INFOCOM", "", "", ""],
    ]
    proxy = {
        'http' : '',
        'https': '',
    }
    
    session = cloudscraper.create_scraper()
    if(os.access('headers.txt', os.R_OK)):
        with open('headers.txt', 'r') as f:
            content = f.read()
            if(content):
                out_print('Load headers.txt')
                lines = content.split('\n')
                tmp = {}
                for v in lines:
                    v = v.split(': ')
                    tmp[v[0]] = v[1]

                session.headers.update(tmp)

    if(os.access('cookies.txt', os.R_OK)):
        with open('cookies.txt', 'r') as f:
            content = f.read()
            if(content):
                out_print('Load cookies.txt')
                domains = content.split('\n\n')
                for domain in domains:
                    lines = domain.split('\n')
                    tmp = {}
                    for v in lines[1].split('; '):
                        v = v.split('=')
                        session.cookies.set(v[0], v[1], domain=lines[0])

    '''
    Matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher, abstract], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher, abstract]]
    '''
    paper_lists = []

    if(os.access('abstract_crawler_input.json', os.R_OK)):
        with open('abstract_crawler_input.json', 'r') as f:
            target = json.loads(f.read())
            out_print("Handle abstract_crawler_input.json")
            tmp = main_handler(target, 1)
            if(tmp):
                paper_lists += tmp

    if(search_list):
        tmp = main_handler(search_list, 1)
        if(tmp):
            paper_lists += tmp

    out_print('Sum: ' + str(len(paper_lists)))
    open('abstract_crawler_output.json', 'w').write(json.dumps(paper_lists))
    out_print('END')
    
