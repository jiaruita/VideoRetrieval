import solr
import re

days = '(0[1-9]|1[0-9]|2[0-9]|30|31|[1-9])'
month_number = '(0[1-9]|10|11|12|[1-9])'
month_short = '(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
month_full = '(january|february|march|april|may|june|july|august|september|october|november|december)'
month = '(' + month_number + '|' + month_short + '|' + month_full + ')'
years = '((19|20)?\d\d)'
template = '(?P<year>' + years + ')' + '[^a-zA-Z0-9]?' + '(?P<month>' + month + ')' + '[^a-zA-Z0-9]?' + '(?P<day>' + days + ')' 
re_date = re.compile(template)
months_list = (['jan', 'feb', 'mar', 'apr', 'may', 'jun'
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])

re_word_and_number = '\d+\.?\d+|[\w]+'
class MyTokenizer:
    def __init__(self, regexp):
        self.reg = regexp
    def tokenize(self, text):
        from nltk.tokenize import RegexpTokenizer
        tokenizer = RegexpTokenizer(self.reg)
        tokens = tokenizer.tokenize(text)
        return tokens


def initiation():
    """connect to solr server"""
    s = solr.SolrConnection('http://localhost:8983/solr')
    return s



def search(sconn, query):
    """search and return the results"""
    query_dict = query_proc(query)
    sort = ''
    string = query_dict['string']
    if query_dict['sort'] != '':
        sort = query_dict['sort']
    response = sconn.query(string, sort = sort)
    return response.results

def query_proc(query):
    """process the query, extract information, return the query parameters"""
    contain_date = True
    query_dict = {}
    string = ''
    date_string = ''
    sort_string = ''
    #process the query and get a list of tokens
    query = query.lower().strip('\n ')
    tokenizer = MyTokenizer(re_word_and_number)
    tokens = tokenizer.tokenize(query)

    #extract date information from the query
    query_no_space = re.compile('\s+').sub('', query)
    m = re_date.search(query_no_space)
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
        weight = float(date)
        date_string = 'weight:[' + str(weight) + ' TO *]'
    else:
        contain_date = False
    
    terms = []
    for token in tokens:
        terms.append('title:' + token)
        terms.append('description:' + token)
    #string is the parameter of solr request
    string = ' OR '.join(terms)
    if contain_date == True:
        string = '(' + string + ') OR ' + date_string
        sort_string = 'weight'
    
    query_dict['string'] = string
    query_dict['sort'] = sort_string
    return query_dict


def call(query):
    """called by user interface"""
    s = initiation()
    #query = raw_input('query:\n')
    results = search(s, query)
    return results

def run():
    """used to test"""
    s = initiation()
    query = raw_input('query:\n')
    results = search(s, query)
    for item in results:
        print item
    return results

