from Module_MetaClass import Crawler
import datetime
import requests
from html.parser import HTMLParser
import time
import json
def clean_parsed_data(data,source):
    for news in data:
        #清除如\r \d等
        for i in news.keys():
            if type(news[i])==str:
                for delete in ['\r','\d','\n']:
                    news[i] = news[i].replace(delete,'')
        try:news['link'] = news.pop('url') 
        except:pass
        try:news['pubdate'] = news.pop('publishedAt')
        except:pass
        try:news['pubdate'] = news.pop('pubDate')
        except:pass
        if 'author' not in news:
            news['author']=None
        if 'source' not in news:
            news['source']=source
    return data
#用來以特定模式抓取RSS資料的parser
class RSS_Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cur_stag = []   # list
        self.content = []    # dic in list [{}, {}]

    def handle_starttag(self, tag, attrs):
        self.cur_stag.append(tag)
        if tag == 'item':
            self.content.append({})

    def handle_endtag(self, tag):
        self.cur_stag.pop()

    def handle_data(self, data):
        if len(self.cur_stag) >= 4 and \
                 'item' in self.cur_stag:
            self.content[-1].update({self.cur_stag[-1]:data})

class RSS(Crawler):
    def __init__(self, Name, Source):
        self.Name = Name
        self.Source = Source
        
    def CrawlerRawData(self):
        self.RawData = requests.get(self.Source).text
        return (self)

    def __RecordCrawlerTime(self):
        return (datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M%S"))

    def ParseRawData(self):
        # self.ParsedData = feedparser.parse(self.RawData)
        self.CrawlerTime['Start'] = self.__RecordCrawlerTime()
        parser = RSS_Parser()
        parser.feed(self.RawData)
        cleaned = clean_parsed_data(parser.content,self.Name)
        self.ParsedData = cleaned
        self.CrawlerTime['End'] = self.__RecordCrawlerTime()
    def Close(self):
        return(self.ParsedData)

class API(Crawler):
    RawData = ''
    CrawlerTime = {'Start': 19000101000000, 'End': 21001231235959}
    ParsedData = [{}]

    def __init__(self, Name, Source):
        self.Name = Name
        self.Source = Source

    def CrawlerRawData(self):
        response = requests.get(self.Source)
        retry = 0
        while response.status_code != 200 and retry < 3:
            try:
                response = requests.get(self.Source)
                time.sleep(1)
                retry = 10
            except Exception:
                retry = retry + 1
                time.sleep(1)
        self.RawData = response.text
        return (self)

    def __RecordCrawlerTime(self):
        return (datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S"))

    def ParseRawData(self):
        self.CrawlerTime['Start'] = self.__RecordCrawlerTime()

        jd = json.loads(self.RawData)
        jd = jd.get('articles')
        for news in jd:
            news['source'] = news['source']['name']
        cleaned = clean_parsed_data(jd,self.Name)
        self.ParsedData = cleaned
        self.CrawlerTime['End'] = self.__RecordCrawlerTime()
    def Close(self):
        return (self.ParsedData)






