import pandas as pd
import json
import numpy as np
import glob
import re
from tqdm import tqdm

# 之前抓歷史資料時，沒有加入pubDate。wsj當天抓的新聞就只有當天的，所以直接用檔名當作pubdate
def modify_historic_news():
    history_news = glob.glob('./parsed_data/*_WSJ.json') 
    for i in history_news:
        x=re.findall(r'\d*-\d*-\d*',str(i))[0]
        with open(i,'r')as f:
            news = json.load(f)
        for j in range(len(news)) :
            news[j].update({'pubdate':x})
            try:del news[j]['pubDate']
            except:pass
        with open(i,'w')as f:
            json.dump(news,f)


# 將全部新聞併起來並且sort pubdate
def concat_news():
    all_news = glob.glob('./parsed_data/*.json')
    df = pd.DataFrame()
    for news in tqdm(all_news):
        with open(news,'r')as f:json_file = json.load(f)
        if json_file == []:
            continue
        else:
            x = pd.read_json(news)
            x['pubdate'] = x['pubdate'].apply(pd.to_datetime)
            df = df.append(x)
            df.drop_duplicates('title',inplace = True)
    df['pubdate'] = df['pubdate'].apply(lambda x:x.strftime('%Y%m%d'))
    #我們用的資料只要在2018年以後，故把以前的新聞
    current = df['pubdate'].apply(lambda x:True if int(x)>=20180101 else False)
    df = df[current]
    df = df.sort_values('pubdate')
    return df

#將每天新聞存成json檔
def generate_everyday_news():
    df = concat_news()
    for date in df.pubdate.drop_duplicates():
        try:
            eachday_news = df.query('pubdate == @date')
            eachday_news = json.loads(eachday_news.to_json(orient = 'records'))
            with open(f'./everyday_news/{date}.json','w')as f:
                json.dump(eachday_news,f)
        #有些日期完全沒有新聞，跳過'20180222', '20181003'
        except:
            print(f'{date} no news')
            pass

if __name__ == '__main__':   
    # modify_historic_news()
    generate_everyday_news()