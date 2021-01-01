import pandas as pd
import json
import glob
from tqdm import tqdm
from gensim.models import Word2Vec
import pickle
import numpy as np

def gen_keywords(start,end):
    total_date = pd.date_range(start,end,freq='d')
    ans = {}
    for dates in tqdm(total_date):
        ans_list = []
        all_similar = []
        date = dates.strftime('%Y%m%d')
        df = pd.read_json(f'./2_weeks_news/{date}.json')
        string = [' '.join(df.title_cleaned.values).split()]
        model = Word2Vec(string)
        
        for all_word in model.wv.vocab.keys():
            similar = model.wv.most_similar(all_word)
            for i in similar:
                all_similar.append(i[0])
        value,count = np.unique(all_similar,return_counts=True)
        
        count_sort_ind = np.argsort(-count)
        value = value[count_sort_ind] ; count = count[count_sort_ind]
        for i in range(len(count)):
            ans_list.append( (value[i],count[i]/len(model.wv.vocab.keys())) )
        ans[date] = ans_list
    with open('top_news_keys','wb')as f:
        pickle.dump(ans,f)
        
if __name__ == '__main__':   
    gen_keywords('2018-01-01','2020-05-26')