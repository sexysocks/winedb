from html.parser import HTMLParser
from collections import defaultdict
import csv
import json
import requests

def create_wine(winedb_url, fields):
    print('Adding wine: '+ fields['name'])
    if 'quantity' in fields.keys():
        del fields['quantity']
    r = requests.post(winedb_url+'/wines/'+fields['fridge']+'/'+fields['shelf'], json.dumps(fields))
    print(r.text)

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self, fields, counts, locations, producers):
        HTMLParser.__init__(self)
        self.tag = ''
        self.fields = fields
        self.counts = counts
        self.total_count = 0
        self.locations = locations
        self.producers = producers

    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3', 'h4', 'b', 'i'):
            self.tag = tag
            return "Encountered a start tag:" + tag

    def handle_endtag(self, tag):
        if tag == 'body':
            print('Added %d wines to the database' % self.total_count)


    def handle_data(self, data):
        # if self.tag in ('h1', 'h2', 'h3', 'h4'):
        #     return "Encountered a data:" + data
        if len(data) > 1:
            if self.tag == 'h1':
                self.fields['category'] = data
                #print(self.fields)
            if self.tag == 'h2':
                self.fields['subcategory'] = data
                #print(self.fields)
            if self.tag == 'h3':
                self.fields['country'] = data
                #print(self.fields)
            if self.tag == 'h4':
                if len(data.split(',')) == 2:
                    self.fields['region'] = data.split(',')[0].strip()
                    self.fields['varietal'] = data.split(',')[1].strip()
                else:
                    self.fields['region'] = data
                    self.fields['varietal'] = data
            if self.tag == 'b':
                if data.startswith('NV'):
                    self.fields['vintage'] = 'NV'
                    self.fields['name'] = data[3:]
                else:
                    self.fields['vintage'] = data[:4]
                    self.fields['name'] = data[5:]

                for p in producers:
                    if self.fields['name'].startswith(p):
                        self.fields['producer'] = p

                self.fields['quantity'] = self.counts[data]
                self.total_count += self.fields['quantity']

                for l in self.locations[data]:
                    if l[0].lower() == 'right wine fridge':
                        self.fields['fridge'] = 'right'
                    elif l[0].lower() == 'left wine fridge':
                        self.fields['fridge'] = 'left'
                    else:
                        self.fields['fridge'] = 'small'
                    self.fields['shelf'] = l[1]
                    create_wine('http://dusticole-winedb.us-east-1.elasticbeanstalk.com/', self.fields)
                    #print(json.dumps(self.fields) + ',')

if __name__=='__main__':
    producers = []
    with open('../data/producers-2017-08-14.csv', 'rt', encoding='raw_unicode_escape') as f:
        reader = csv.reader(f, delimiter='/')
        for row in reader:
            producers += [row[0].strip()]

    # First use labels.csv (CSV with (Barcode, Wine, Label) per wine in Cellartracker database)
    # to build a dictionary for each wine
    counts = defaultdict(int)
    locations = defaultdict(list)
    with open('../data/labels-2017-08-14.csv', 'rt', encoding='raw_unicode_escape') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[1].replace('\n', ' ')
            counts[name] += 1
            locations[name].append([r.strip() for r in row[2].replace('\n', ' ').split('/')])


    # Then build an entry and insert into database using REST API
    fields = {
        'category': '',
        'subcategory': '',
        'country': '',
        'region': '',
        'varietal': '',
        'vintage': '',
        'producer': '',
        'name': '',
        'fridge': '',
        'shelf': '',
        'quantity': 0}


    parser = MyHTMLParser(fields, counts, locations, producers)
    print('[')
    parser.feed(open('../data/wine-2017-08-14.html').read())
    print(']')