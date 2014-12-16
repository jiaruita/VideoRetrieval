from bs4 import BeautifulSoup
import re

days = '(0[1-9]|1[0-9]|2[0-9]|30|31|[1-9])'
month_number = '(0[1-9]|10|11|12|[1-9])'
month_short = '(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
month_full = '(january|february|march|april|may|june|july|august|september|october|november|december)'
month = '(' + month_number + '|' + month_short + '|' + month_full + ')'
years = '((19|20)?\d\d)'
template = '(?P<month>' + month + ')' + '[^a-zA-Z0-9]?' + '(?P<day>' + days + ')' + '[^a-zA-Z0-9]?' + '(?P<year>' + years + ')' 
re_date = re.compile(template)
months_list = (['jan', 'feb', 'mar', 'apr', 'may', 'jun'
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])


class Doc:
    def __init__(self):
        self.fields = []
    def add_field(self, name, text):
        s = '<field name=\"' + name + '\">' + text + '</field>\n'
        self.fields.append(s)
    def write_doc(self, f):
        for field in self.fields:
            f.write(field)
            
def proc_doc(index, url, content):
    """process a doc, extract information, return a object"""
    doc = Doc()
    doc.add_field('id', str(index))
    doc.add_field('url', url)
    soup = BeautifulSoup(content)
    title = str(soup.find(attrs = {'id':'eow-title'}).string).lower()
    title = title.strip('\n ')
    count = soup.find(attrs = {'class':'watch-view-count'}).string
    count = re.compile('\D').sub('',count)
    description = str(soup.find(attrs = {'id':'eow-description'}).string).lower()
    if description == 'no description available.':
        description = ''
    else:
        description = description.strip('\n ')

    # get information about date:
    title_no_space = re.compile('\s+').sub('', title)
    m = re_date.search(title_no_space)
    date = ''
    if m is not None:
        year = m.group('year')
        month = m.group('month')
        day = m.group('day')
        if len(year) == 2:
            if int(year) < 14:
                year = '20' + year
            else:
                year = '19' + year
        if len(month) == 1:
            month = '0' + month
        elif len(month) > 2:
            if month[:3] in months_list:
                month = str(1 + months_list.index(month[:3]))
        if len(day) == 1:
            day = '0' + day
        date = year + month + day

    # weight is the field containing information about date
    doc.add_field('weight', date)
    doc.add_field('title', title)
    doc.add_field('popularity', count)
    doc.add_field('description', description)
    return doc

def write_xml(xml, doc):
    """Parameters:
        xml: xml file to be written
        doc: Doc object that represents a Html file"""
    #xml.write('<add>\n\t<doc>\n')
    xml.write('\t<doc>\n')
    for field in doc.fields:
        xml.write('\t\t' + field)
    xml.write('\t</doc>\n')
    #xml.write('\t</doc>\n</add>')

def read_files():
    """read a file recording URLs of pages in corpus
        then read the corpus"""
    url_file = open('log-cnn.txt')
    page_dir = './corpus'
    url_list = url_file.read().split('\n')
    cnn_xml = open('cnn.xml', 'w')
    cnn_xml.write('<add>\n')
    for index, url in enumerate(url_list):
        page = open(page_dir + '/cnn' + str(index) + '.html')
        doc = proc_doc(index, url, page.read())
        page.close()
        write_xml(cnn_xml, doc)
        if index > 100:
            break
    cnn_xml.write('</add>')
    url_file.close()
    cnn_xml.close()
    
read_files() 
