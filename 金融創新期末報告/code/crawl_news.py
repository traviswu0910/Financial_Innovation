from Module_Clean import Clean
from Module_Crawler import RSS, API
import pandas as pd
import glob
from datetime import datetime
import json

today=datetime.now().strftime('%Y-%m-%d')

def get_RSS_data():
    rss_list = pd.read_excel('RSS_list.xlsx')
    for name, url in zip(rss_list.name, rss_list.url):
        website = RSS(name, url)
        website.CrawlerRawData()
        website.ParseRawData()
        parsed_data = website.Close()
        raw_data = website.RawData

        # save raw data into txt
        with open(f'./raw_data/{today}_{name}.txt', 'w', encoding='utf-8')as f:
            f.write(raw_data)
        # save dictionary to json file
        with open(f'./parsed_data/{today}_{name}.json', 'w')as f:
            json.dump(parsed_data, f)


def get_API_data():
    api_list = pd.read_excel('API_list.xlsx')
    for name, url in zip(api_list.name, api_list.url):
        website = API(name, url)
        website.CrawlerRawData()
        #某個網站錯誤時，顯示錯誤，且跳過
        if json.loads(website.RawData)['status']!='ok':
            print(f'error : {name}')
            continue
        website.ParseRawData()
        parsed_data = website.Close()
        raw_data = website.RawData

        # save raw data into txt
        with open(f'./raw_data/{today}_{name}.txt', 'w', encoding='utf-8')as f:
            f.write(raw_data)
        # save dictionary to json file
        with open(f'./parsed_data/{today}_{name}.json', 'w')as f:
            json.dump(parsed_data, f)

            
if __name__ == '__main__':
    get_RSS_data()
    get_API_data()
    