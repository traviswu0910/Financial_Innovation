import pickle
import pandas as pd
from tqdm import tqdm
import json

with open('top_news_keys','rb')as f:
    key = pickle.load(f)

def gen_topnews(start,end):
    with open('top_news_keys','rb')as f:
        key = pickle.load(f)
    total_date = [x.strftime('%Y%m%d') for x in pd.date_range(start,end,freq='d')]
    for date in tqdm(total_date):
        #取前三大關鍵字
        keys = [i for i,j in key[date][:3]]
        df = pd.read_json(f'./2_weeks_news/{date}.json')
        for i in range(3):
            df[f'count{i+1}'] = df.title_cleaned.apply(lambda x:x.split().count(keys[i]))
        df=df.sort_values(['pubdate','source'],ascending=False)
        #將關鍵字填入list中第一項，之後UI抓值用
        top_news_1 = json.loads(df.query('count1 > 0').to_json(orient = 'records'))
        top_news_1.insert(0,keys[0])
        top_news_2 = json.loads(df.query('count2 > 0').to_json(orient = 'records'))
        top_news_2.insert(0,keys[1])
        top_news_3 = json.loads(df.query('count3 > 0').to_json(orient = 'records'))
        top_news_3.insert(0,keys[2])
        
        # with open(f'./top_news/{date}_1.json','w')as f:
        #     json.dump(top_news_1,f)
        # with open(f'./top_news/{date}_2.json','w')as f:
        #     json.dump(top_news_2,f)
        # with open(f'./top_news/{date}_3.json','w')as f:
        #     json.dump(top_news_3,f)

        with open(f'C:\\Users\\Bruce\\南山\\NewsAssistant\\UIData\\news\\{date}_1.json','w')as f:
            json.dump(top_news_1,f)
        with open(f'C:\\Users\\Bruce\\南山\\NewsAssistant\\UIData\\news\\{date}_2.json','w')as f:
            json.dump(top_news_2,f)
        with open(f'C:\\Users\\Bruce\\南山\\NewsAssistant\\UIData\\news\\{date}_3.json','w')as f:
            json.dump(top_news_3,f)

if __name__ == '__main__':   
    gen_topnews('2018-01-02','2020-05-26')
    