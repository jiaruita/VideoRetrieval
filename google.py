# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import urllib2
import StringIO
import gzip
import HTMLParser
import time
import random
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':'www.google.com' 
             }
req_timeout = 100
directory = 'corpus/'
#source = 'source/'
index = 0

def one_page_google(soup, log):
    h3_list = soup.findAll('h3')
    for h3 in h3_list:
        href = h3.find('a')['href']
 #       url_list.append(href)
        log.write(href + '\n')
        try:
            save_page(href)
        except:
            print 'except:' + str(index) + ': ' + href

def one_page_56(soup, log):
    item_list = soup.find(id = 'soSwitch').findAll('h6')
    for h6 in item_list:
        href = h6.find('a')['href']
        log.write(href + '\n')
        time.sleep(3 * random.random() + 2)
        try:
            save_page(href)
        except:
            print 'except: ' + str(index) + ': ' + href

def one_page_youtube(soup, log):
    item_list = soup.find(id = 'search-results').findAll(attrs = {'class': 'yt-lockup2-title'})
    for title in item_list:
        href = title.find('a')['href']
        if not href[:5] == 'http:':
            href = 'http://www.youtube.com' + href
        log.write(href + '\n')
        time.sleep(3 * random.random() + 2)
        try:
            save_page(href)
        except:
            print 'except: ' + str(index) + ': ' + href
        
def next_page(soup, site):
    if site == 'google':
        href = soup.find(id = 'pnnext')['href']
    elif site == 'baidu':
        href = soup.findAll(attrs = {'class': 'n'})[-1]['href']
    elif site == '56':
        temp = soup.find(attrs = {'class': 'mod56_page_pn'})
        href = temp.findAll('a')[-1]['href']
    elif site == 'youtube':
        temp = soup.find(attrs = {'class': 'yt-uix-pager'})
        href = temp.findAll('a')[-1]['href']
    if not href[:5] == 'http:':
        href = 'http://www.' + site + '.com' + href
    return href


def fetch(url):
    req = urllib2.Request(url, None, req_header)
    resp = urllib2.urlopen(req, None, req_timeout)
    html = resp.read()
    if resp.headers.get('content-encoding', None) == 'gzip':
        html = gzip.GzipFile(fileobj = StringIO.StringIO(html)).read()
    return html

def save_page(url):
    global index
    name = directory + 'cnn' + str(index) + '.html'
    html = fetch(url)
    f = open(name, 'w')
    f.write(html)
    f.close()
    index += 1
    print 'save_page: ' + name + ': ' + url + '\n'
    

def iter_page(start_soup):
    html_parser = HTMLParser.HTMLParser()
 #   url_list = []
    log = open('log-cnn.txt', 'w')
    for i in range(1,50):
        one_page_youtube(start_soup, log)
        next_url = next_page(start_soup, 'youtube')
        next_url = html_parser.unescape(next_url)
        print 'next url: ' + next_url
        time.sleep(10*random.random()+5)
        """print repr(next_url)
        u = repr(next_url)[1:-1]
        d = '%E5%A4%A7%E5%AD%A6%E7%94%9F%E4%BA%86%E6%B2%A1'
        u = u[:23] + d + u[53:]
        print u"""
        #print type(next_url)
        next_url = next_url.encode('utf-8')
        #print type(next_url)
        html = fetch(next_url)
        start_soup = BeautifulSoup(html)
        i += 1
    print index
    log.close()

def run():
    #cnn.html is the result page from youtube
    f = open('cnn.html')
    s = f.read()
    soup = BeautifulSoup(s)
    f.close()
    iter_page(soup)

run()
    
