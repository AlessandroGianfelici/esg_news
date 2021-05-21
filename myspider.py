# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

matchMont = {'gennaio' : 1,
'febbraio' : 2,
'marzo' : 3,
'aprile' : 4,
'maggio' : 5,
'giugno' : 6,
'luglio' : 7,
'agosto' : 8,
'settembre' : 9,
'ottobre' : 10,
'novembre' : 11,
'dicembre' : 12}

def parse_data(datastr):
    giorno = int(datastr[:2])
    mese = matchMont[datastr[3:-5].lower()]
    anno = int(datastr[-4:])
    return datetime(anno, mese, giorno)

def parseText(soup):
    all_paragraph = soup.find("article").find_all('p')
    return ' '.join([par.get_text() for par in all_paragraph])

def file_folder_exists(path: str):
    """
    Return True if a file or folder exists.
    :param path: the full path to be checked
    :type path: str
    """
    try:
        os.stat(path)
        return True
    except:
        return False

def select_or_create(path: str):
    """
    Check if a folder exists. If it doesn't, it create the folder.
    :param path: path to be selected
    :type path: str
    """
    if not file_folder_exists(path):
        os.makedirs(path)
    return path

outputpath = select_or_create('json')

class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = ['esgnews.it']
    start_urls = [r'https://esgnews.it']
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )

    def parse_item(self, response):
        if "esgnews.it" in response.url:
            try:
                filename = response.url.split("/")[-2] + '.json'
                soup = BeautifulSoup(response.body, 'html.parser')
                date = parse_data(soup.find("article").find('time').text)
                text = parseText(soup)
                category = soup.find("article").find_all('h4')[0].get_text()
                title = soup.find("article").find_all('h1')[0].get_text()
                with open(os.path.join(outputpath, filename), 'w') as outfile:
                    json.dump({'date': f'{date:%Y%m%d}', 
                               'category' : category,
                               'title' : title,
                               'text': text}, outfile)
                
            except:
                pass#time.sleep(100)
        self.log('crawling'.format(response.url))
