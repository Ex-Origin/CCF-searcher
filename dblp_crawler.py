#!/usr/bin/python3

from unittest import result
import requests
import re
import time
import html
import urllib
import json
import os

ccf_json_path = 'CCF_rank_2019.json'
ccf_rank = []
ccf_abbreviation = []
ccf_abbreviation_lower = []
ccf_full_name_hash = []
ccf_full_name = []
ccf_publisher = []
ccf_url = []

def out_print(info:str):
    print('[%s] : %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), info), flush=True)

def hash_full_name(name:str)->str:
    name = name.lower()
    r = ''
    for v in name:
        if(v >= 'a' and v <= 'z'):
            r += v
    return r

def ccf_find_by_abbreviation(abbreviation, inner_url)->int:
    if(not abbreviation):
        return -1

    result = -1
    if(abbreviation in ccf_abbreviation):
        tmp = ccf_abbreviation.index(abbreviation)
        if(inner_url in ccf_url[tmp]):
            return tmp

    abbreviation = abbreviation.lower()
    for i in range(len(ccf_abbreviation)):
        if(abbreviation == ccf_abbreviation_lower[i] and inner_url in ccf_url[i]):
            result = i
            break

    return result

def ccf_find_by_name(pre_name, inner_url)->int:
    if(not pre_name):
        return -1

    name = hash_full_name(pre_name)

    result = -1
    if(name in ccf_full_name_hash):
        tmp = ccf_full_name_hash.index(name)
        if(inner_url in ccf_url[tmp]):
            return tmp

    max_len = 0
    for i in range(len(ccf_full_name_hash)):
        if(ccf_full_name_hash[i] in name and inner_url in ccf_url[i]):
            if(len(ccf_full_name_hash[i]) > max_len and ccf_full_name[i].count(' ') >= 2):
                max_len = len(ccf_full_name_hash[i])
                result = i
                    
    return result

def specify_abbreviation(url):
    origin = ''
    if(url[-1] == '/'):
        head = url.rfind('/', 0, -1)
        if(head != -1):
            origin = url[head + 1 : -1].upper()
        else:
            out_print('Error url %s' % (url))
    else:
        head = url.rfind('/')
        if(head != -1):
            origin = url[head + 1 : ].upper()
        else:
            out_print('Error url %s' % (url))
    return origin

# old_list must be matrix
def add_new_column(old_list, position, value=''):
    new_list = []
    for v in old_list:
        new_row = v[:position] + [value] + v[position:]
        new_list += [new_row]
    return new_list

def get(url, proxy={}):
    i = 0
    raw_response = False
    while(i < 5 and raw_response == False):
        i += 1
        try:
            raw_response = requests.get(url, proxies=proxy)
        except Exception as e:
            out_print(str(e))
            time.sleep(10)
    if(raw_response.status_code == 404):
        out_print('HTTP 404 at %s' % (url))
        return ''
    else:
        text = raw_response.text
        text_without_line = text.replace('\n', '')
        return text_without_line

def single_conf_handler(url, proxy={}):
    '''
    Return matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    year = -1
    tmp = re.findall('[^\d]([12]\d\d\d)w{0,1}\.html$', url)
    if(tmp):
        year = int(tmp[0])

    text_inner_without_line = get(url, proxy)
    if(text_inner_without_line == ''):
        out_print("single_conf_handler ERROR")
        return []

    single_item_list = re.findall('<li class="entry (.+?)</cite>', text_inner_without_line)
    
    # The year in web content instead of url
    tmp = re.findall('<span itemprop="datePublished">([12]\d\d\d)</span>', single_item_list[0])
    if(tmp):
        tmp = int(tmp[0])
    else:
        tmp = re.findall('[12]\d\d\d', text_inner_without_line)
        if(tmp):
            tmp = int(tmp[0])
            out_print('Unstable year search (result: %d) at %s' % (tmp, url))
        else:
            tmp = -1
            out_print('Unstable year search Failed at %s' % (url))
        
    if(year == -1):
        year = tmp
    elif(abs(tmp - year) > 3):
        out_print('Url year(%d) is different from content year(%d) at %s' % (year, tmp, url))

    name = re.findall('<span class="title" itemprop="name">(.+?)\.{0,1}</span>', single_item_list[0])[0]
    name = html.unescape(re.sub('<.+?>', '', name))

    abbreviation = ''
    tail = url.rfind('.')
    head = url.rfind('/')
    if(tail != -1 and head != -1):
        tmp = re.findall('[a-zA-Z]+', url[head:tail])
        if(tmp):
            abbreviation = tmp[0].upper()
        else:
            out_print('Not found abbreviation in %s' % (url))

    index = ccf_find_by_abbreviation(abbreviation, 'dblp.uni-trier.de/db/conf')
    if(index == -1 and name):
        index = ccf_find_by_name(name, 'dblp.uni-trier.de/db/conf')

    tmp_paper = []
    for single_item in single_item_list:
        
        head = single_item.find('<div class="head"><a href="')
        tail = single_item.find('"', head + 27)
        
        doi_url = ''
        if(head != -1 and tail != -1):
            doi_url = single_item[head + 27:tail]

        authors = html.unescape(', '.join(re.findall('<span itemprop="name" title=".+?">(.+?)</span>', single_item)))
            
        title = re.findall('<span class="title" itemprop="name">(.+?)\.{0,1}</span>', single_item)[0]
        title = html.unescape(re.sub('<.+?>', '', title))

        if(index != -1):
            tmp_paper += [[year, title, doi_url, authors, ccf_rank[index], ccf_abbreviation[index], ccf_full_name[index], name, ccf_publisher[index]]]
        else:
            tmp_paper += [[year, title, doi_url, authors, 'CCF-None', abbreviation, '', name, '']]
            
    return tmp_paper

def single_journals_handler(url, proxy={}):
    '''
    Return matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    text_inner_without_line = get(url, proxy)
    if(text_inner_without_line == ''):
        out_print("single_journals_handler ERROR")
        return []

    name = re.findall('<h1>(.+?)\.{0,1}</h1>', text_inner_without_line)[0]
    name = html.unescape(re.sub('<.+?>', '', name))

    abbreviation = ''
    tail = url.rfind('.')
    head = url.rfind('/')
    if(tail != -1 and head != -1):
        tmp = re.findall('[a-zA-Z]+', url[head:tail])
        if(tmp):
            abbreviation = tmp[0].upper()
        else:
            out_print('Not found abbreviation in %s' % (url))
    
    index = ccf_find_by_abbreviation(abbreviation, 'dblp.uni-trier.de/db/journals')
    if(index == -1 and name):
        index = ccf_find_by_name(name, 'dblp.uni-trier.de/db/journals')

    tail = 0
    head = 0
    year = -1
    tmp_paper = []
    while(tail != -1 and head != -1):
        head = text_inner_without_line.find('<header><h2', tail)
        if(head != -1):
            tail = text_inner_without_line.find('<header><h2', head + 1)
        if(tail == -1):
            # The last item
            tail = text_inner_without_line.find('<div id="top">', head + 1)

        if(head != -1 and tail != -1):
            item = text_inner_without_line[head:tail]
            tail2 = item.find('</header>')

            tmp = re.findall('[12]\d\d\d', item[:tail2])
            if(tmp):
                year = int(tmp[0])
            else:
                tmp = re.findall('<h1>(.+?)</h1>', text_inner_without_line)
                if(tmp):
                    tmp = re.findall('[12]\d\d\d', tmp[0])
                    if(tmp):
                        year = int(tmp[0])
                    else:
                        out_print('Not found year in %s , use previous item %d' % (url, year))
                else:
                    out_print('Not found year in %s , use previous item %d' % (url, year))

            single_item_list = re.findall('<li class="entry (.+?)</cite>', item)

            for single_item in single_item_list:

                head2 = single_item.find('<div class="head"><a href="') + 27
                tail2 = single_item.find('"', head2)

                doi_url = ''
                if(head != -1 and tail != -1):
                    doi_url = single_item[head2:tail2]

                authors = html.unescape(', '.join(re.findall('<span itemprop="name" title=".+?">(.+?)</span>', single_item)))

                title = re.findall('<span class="title" itemprop="name">(.+?)\.{0,1}</span>', single_item)[0]
                title = html.unescape(re.sub('<.+?>', '', title))

                if(index != -1):
                    tmp_paper += [[year, title, doi_url, authors, ccf_rank[index], ccf_abbreviation[index], ccf_full_name[index], name, ccf_publisher[index]]]
                else:
                    tmp_paper += [[year, title, doi_url, authors, 'CCF-None', abbreviation, '', name, '']]

    return tmp_paper

def conf_handler(url, proxy={}):
    '''
    Return matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    text_without_line = get(url, proxy)
    if(text_without_line == ''):
        out_print("conf_handler ERROR")
        return []

    all_conferences = re.findall('<nav class="publ">(.+?)</nav>', text_without_line) # conferences

    detail_url_list = []
    for single_ul in all_conferences:
        head = single_ul.find('href="')
        tail = single_ul.find('"', head + 6)
        tmp = single_ul[head + 6: tail]
        if('dblp.uni-trier.de' in tmp):
            detail_url_list += [tmp]
        else:
            out_print('Unsupported conference sub item %s' % (tmp))
    
    paper_info = []
    for detail_url in detail_url_list:
        paper_info += single_conf_handler(detail_url, proxy)

    return paper_info
    
def journals_handler(url, proxy={}):
    '''
    Return matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    text_without_line = get(url, proxy)
    if(text_without_line == ''):
        out_print("journals_handler ERROR")
        return []

    all_journals = re.findall('<ul>(.+?)</ul>', text_without_line)
    li_list = ''
    for ul_inner in all_journals:
        if(ul_inner.find('Volume') != -1):
            li_list = ul_inner
            break
    detail_url_list = re.findall('href="(.+?)"', li_list)

    abbreviation = specify_abbreviation(url)

    paper_info = []
    for detail_url in detail_url_list:
        paper_info += single_journals_handler(detail_url, proxy)
    
    return paper_info

def load_ccf():
    global ccf_rank
    global ccf_abbreviation
    global ccf_abbreviation_lower
    global ccf_full_name_hash
    global ccf_full_name
    global ccf_publisher
    global ccf_url

    if(os.access(ccf_json_path, os.R_OK)):
        with open(ccf_json_path, 'r') as f:
            lists = json.loads(f.read())
            for item in lists:
                ccf_rank += [item['ccf-rank']]
                ccf_abbreviation += [item['abbreviation']]
                ccf_abbreviation_lower += [item['abbreviation'].lower()]
                ccf_full_name_hash += [hash_full_name(item['full-name'])]
                ccf_full_name += [item['full-name']]
                ccf_publisher += [item['publisher']]
                ccf_url += [item['url']]

def main_handler(search_list, start=1, proxy={}):
    '''
    Return matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    load_ccf()

    length = len(search_list)
    num = length - (start - 1)
    paper_info = []
    for i in range(num):
        instance_url = search_list[(start - 1) + i]
        out_print('(%03d/%03d) Deal with: %s' % (start + i, length, instance_url))

        if('dblp.uni-trier.de/db/conf' in instance_url):
            paper_info += conf_handler(instance_url, proxy)
        elif('dblp.uni-trier.de/db/journals' in instance_url):
            paper_info += journals_handler(instance_url, proxy)
        else:
            out_print('Only support for dblp.uni-trier.de')
    
    return paper_info

def get_unique_ccf_url(path=ccf_json_path)->list:
    '''
    Get all CCF links
    '''
    result = []

    if(os.access(path, os.R_OK)):
        with open(path, 'r') as f:
            lists = json.loads(f.read())
            for item in lists:
                if(item['url']):
                    result += [item['url']]

    return list(set(result))

if(__name__ == '__main__'):
    search_list = [
        # 'http://dblp.uni-trier.de/db/conf/ppopp/',
        # 'http://dblp.uni-trier.de/db/journals/tocs/',
    ]
    proxy = {
        'http': '',
        'https': '',
    }
    '''
    Matrix 
    [[year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher], 
     [year, title, doi_url, authors, ccf_rank, abbreviation, ccf_name, full_name, publisher]]
    '''
    paper_lists = []

    paper_lists += main_handler(get_unique_ccf_url(), 1, proxy)

    if(search_list):
        paper_lists += main_handler(search_list, 1, proxy)

    out_print('Sum: ' + str(len(paper_lists)))
    open('dblp_crawler_output.json', 'w').write(json.dumps(paper_lists))
    out_print("END")
    