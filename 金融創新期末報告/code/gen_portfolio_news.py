import pandas as pd
import json
from tqdm import tqdm
from Module_Clean import Clean

fullName = pd.read_json("./Schema/Reference/InfoCodeToFullName.json").set_index('InfoCode')
synonym = pd.read_json("./Schema/Reference/Synonym.json").set_index('InfoCode')

strategies = ['PortfolioList_AbovePositive5','PortfolioList_BelowNegative5',
            'PortfolioList_WeekAbovePositive10','PortfolioList_WeekBelowNegative10',
            'PortfolioList_MonthAbovePositive20']

def get_syn_intersection(df,syn):
    '''
    用來比對新聞標題是否包含公司名稱，並且將包含哪些公司名稱存成list
    input為dataframe
        df:新聞
        syn:公司名稱、同義詞
    '''
    #special word 將兩個字併起來，並且中間加上 _ 以便找尋 synonym，如AAPL US併成AAPL_US
    def get_special_word(news):
        news_title = news.split()
        special_word = Clean(news);special_word.Separate(2);special_word = special_word.Text
        special_word = list(map(lambda x:x.replace(' ','_'),special_word))
        news_title.extend(special_word)
        return news_title
    df['title_add_special'] = df['title_cleaned'].apply(lambda x:get_special_word(x))
    df = df.reset_index(drop=True)
    def get_company(news_title):
        intersection=[]
        title = set(news_title)
        for co in syn.index:
            syn_word = set(syn.loc[co].Synonym)
            #如果標題中含有公司的同義字，就把公司名稱加入list中
            if len(title & syn_word)>0:
                intersection.extend([fullName.loc[co].Name])
        return intersection

    df['title_company'] = df['title_add_special'].apply(lambda x:get_company(x))
    df['count'] = df['title_company'].apply(lambda x:1 if len(x)>0 else 0)
    del df['title_add_special']
    return df

def gen_portfolio_news():
    for strategy in tqdm(strategies):
        df=pd.read_json(f'./Schema/UIFocus/{strategy}.json').set_index('Date')
        #去掉沒有投組的天數
        df = df[df.InfoCode.astype(bool)]
        for date in tqdm(df.index):
            portfolio = df.loc[date].InfoCode
            #########有些明淇選出的股票不在synonym中，有可能是明淇在抓SP500時已經更新成分股了
            port_list = []
            for i in portfolio:
                #有在synonym中的公司才抓
                if i in synonym.index.to_list():
                    port_list.append(i)
            portfolio = port_list
            #############################
            #這天的portfolio 有哪幾間公司(全名)
            portfolio_list = fullName.loc[portfolio].Name.to_list()
            
            synonym_list = synonym.loc[portfolio]
            news = pd.read_json(f'./2_weeks_news/{date}.json').reset_index(drop=True)
            portfolio_news = get_syn_intersection(news,synonym_list)
            portfolio_news = portfolio_news.query('count == 1')
            portfolio_news.sort_values(['pubdate','source'],ascending=False)
            ans = json.loads(portfolio_news.to_json(orient = 'records'))
            ans.insert(0,portfolio_list)
            with open(f'./portfolio_news/news_{strategy}_{date}.json','w')as f:
                json.dump(ans,f)
                    
                    
if __name__ == '__main__':
    gen_portfolio_news()
    

