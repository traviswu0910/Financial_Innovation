import pandas as pd
import json
from tqdm import tqdm
import glob
from Module_Clean import Clean
#將title 清理，去除關鍵字等等
def clean_title(x):
    x=Clean(x)
    x.Capitalize()
    x.DeletePunctuation()
    x.DeleteRedundant()
    return x.Text

def gen_2_week_news(start,end):
    '''5
    example：start = '2019-01-01', end = '2020-05-25'
    '''
    total_date = pd.date_range(start,end,freq='d')
    
    for date in tqdm(total_date):
        two_week_range = pd.date_range(date-pd.to_timedelta(2, 'w'),date,freq='d')
        df=pd.DataFrame()
        for days in two_week_range:
            day = days.strftime('%Y%m%d')
            try:
                files = glob.glob(f'everyday_news/{day}.json')
                for file in files:
                    x=pd.read_json(file)
                    df= pd.concat([df,x])
            except:pass
                
        df = df.drop_duplicates('title')
        df = df.dropna(subset=['title'])
        #排序(最新的在前面)
        df = df.sort_values('pubdate', ascending=False)
        df['title_cleaned'] = df['title'].apply(clean_title)
        x=date.strftime('%Y%m%d')
        with open(f'./2_weeks_news/{x}.json','w')as f:
            ans = json.loads(df.to_json(orient = 'records'))
            json.dump(ans,f)


if __name__ == '__main__':   
    gen_2_week_news('2018-01-01','2020-05-26')