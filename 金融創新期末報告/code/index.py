from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt

app = Flask(__name__)
fullName = pd.read_json("./schema/InfoCodeToFullName.json").set_index('InfoCode')
method_list = {'pph_1':'news_PortfolioList_AbovePositive5',
               'pph_2':'news_PortfolioList_BelowNegative5',
               'pph_3':'news_PortfolioList_WeekAbovePositive10',
               'pph_4':'news_PortfolioList_WeekBelowNegative10',
               'pph_5':'news_PortfolioList_MonthAbovePositive20'
               }
@app.route("/")
def main():
    return render_template('login_willy.html')

@app.route("/login_willy.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        global user
        user = request.values['usr']
        pwd = request.values['pwd']
        with open(f'./schema/Info.json', 'r') as json_file:
            data = json.load(json_file)
        if user not in data.keys():
            data.update({user:{}})
        with open(f'./schema/Info.json', 'w') as json_file:
            json.dump(data, json_file)
            json_file.close()
            
        default_year = '05/05/2020'
        selected = {'pph_1':'','pph_2':'selected','pph_3':'','pph_4':'','pph_5':''}
        default_method = 'pph_2'
        key1,top_news_1 = get_top_news(default_year, 1,'')
        key2,top_news_2 = get_top_news(default_year, 2,'')
        key3,top_news_3 = get_top_news(default_year, 3,'')
        portfolio_list,portfolio_news = get_portfolio_news(default_year,default_method,'')
        if portfolio_list !='':
            ret = get_chart_data(default_year,default_method)
        else :ret=''
        tw_key1,top_tw_1 = get_top_twitter(default_year,1)
        tw_key2,top_tw_2 = get_top_twitter(default_year,2)
        tw_key3,top_tw_3 = get_top_twitter(default_year,3)
        tw_key4,top_tw_4 = get_top_twitter(default_year,4)
        tw1,tw2,tw3 = get_hot_twitter(default_year)
        return render_template("main.html",
                               date = default_year,
                               selected = selected,
                               portfolio = portfolio_list,
                               portfolio_news = portfolio_news,
                               keyword = '',
                               key1 = key1, top_news_list_1 = top_news_1,
                               key2 = key2, top_news_list_2 = top_news_2,
                               key3 = key3, top_news_list_3 = top_news_3,
                               ret=ret,
                                twitter_key_1 = tw_key1, twitter_top_1 = top_tw_1,
                                twitter_key_2 = tw_key2, twitter_top_2 = top_tw_2,
                                twitter_key_3 = tw_key3, twitter_top_3 = top_tw_3,
                                twitter_key_4 = tw_key4, twitter_top_4 = top_tw_4,
                                twitter_pop_1 = tw1,twitter_pop_2 = tw2,twitter_pop_3 = tw3
                               )
    
        
@app.route("/main.html", methods=["POST", "GET"])
def op():
    if request.method == "POST":
        year = request.values['datepicker']
        portfolio = request.values['portfolio']
        keyword = request.form['ikeyword']
        with open(f'./schema/Info.json', 'r') as json_file:
           data = json.load(json_file)
        int = 0
        try:
            while str(int) in data[user].keys():
                int = int + 1
        except:
            return render_template('login.html')
        data[user].update({int : {"date" : year,
                                    "pf" : portfolio,
                                    "kw" : keyword }})
        with open(f'./schema/Info.json', 'w') as json_file:
           json.dump(data, json_file)
        selected = {'pph_1':'','pph_2':'','pph_3':'','pph_4':''}
        selected[portfolio]='selected'
        date = pd.to_datetime(year).strftime('%m/%d/%Y')
        key1,top_news_1 = get_top_news(year, 1,keyword)
        key2,top_news_2 = get_top_news(year, 2,keyword)
        key3,top_news_3 = get_top_news(year, 3,keyword)
        portfolio_list,portfolio_news = get_portfolio_news(year,portfolio,keyword)
        if portfolio_list !='':
            ret = get_chart_data(year,portfolio)
        else: ret=''
        tw_key1,top_tw_1 = get_top_twitter(year,1)
        tw_key2,top_tw_2 = get_top_twitter(year,2)
        tw_key3,top_tw_3 = get_top_twitter(year,3)
        tw_key4,top_tw_4 = get_top_twitter(year,4)
        tw1,tw2,tw3 = get_hot_twitter(year)
        return render_template("main.html",
                               date = date,
                               selected = selected,
                               portfolio = portfolio_list,
                               portfolio_news = portfolio_news,
                               keyword = keyword,
                               key1 = key1, top_news_list_1 = top_news_1,
                               key2 = key2, top_news_list_2 = top_news_2,
                               key3 = key3, top_news_list_3 = top_news_3,
                               ret=ret,
                                twitter_key_1 = tw_key1, twitter_top_1 = top_tw_1,
                                twitter_key_2 = tw_key2, twitter_top_2 = top_tw_2,
                                twitter_key_3 = tw_key3, twitter_top_3 = top_tw_3,
                                twitter_key_4 = tw_key4, twitter_top_4 = top_tw_4,
                                twitter_pop_1 = tw1,twitter_pop_2 = tw2,twitter_pop_3 = tw3
                               )

def get_top_news(which_day,num,keyword):
    which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
    with open(f'./UIData/news/{which_day}_{num}.json')as f:
        file = json.load(f)
        key = file[0]
        news = file[1:]
    news = pd.DataFrame.from_records(news)
    news = news[['title','link','pubdate','source']]
    news = json.loads(news.to_json(orient='records'))
    if keyword != '':
        keyword = keyword.upper()
        choose = []
        for i in news:
            title = i['title'].upper().split()
            if keyword in title:
                choose.append(i)
        news = choose

    return key,news
            
def get_portfolio_news(which_day,method,keyword):
    which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
    method = method_list[method]
    try:
        with open(f'./UIData/news/{method}_{which_day}.json')as f:
            file = json.load(f)
        if len(file)>1:
            portfolio = file[0]
            news = file[1:]
            
            news = pd.DataFrame.from_records(news)
            news['title_company'] = news['title_company'].apply(lambda x:x[0])
            news = news.sort_values(['title_company','pubdate','source'],ascending=[True,False,True])
            news = news[['title','link','pubdate','source','title_company']]
            news = json.loads(news.to_json(orient='records'))
        #當該投組 沒有新聞時
        else :
            portfolio = file[0]
            news = ''
        if keyword != '':
            keyword = keyword.upper()
            choose = []
            for i in news:
                title = i['title'].upper().split()
                if keyword in title:
                    choose.append(i)
            news = choose
        return portfolio,news
    except:
        portfolio = ''
        news = ''
        return portfolio,news
def get_chart_data(which_day,method):
    which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
    method = method_list[method].replace('news_PortfolioList_','')
    data = pd.read_json(f'./UIData/chart/PortfolioPerformance_{method}_{which_day}.json')
    data['company'] = data['InfoCode'].apply(lambda x:fullName.loc[int(x)][0])
    data['Single']=data['Single']*360
    data=data.rename(columns={'Single':'day','Nearest7DaysAnnualSingle':'week',
                              'Nearest30DaysAnnualSingle':'month','Nearest365DaysAnnualSingle':'year'})
    data = data[['company','day','week','month','year']]
    if len(data)>20:
        if method=='AbovePositive5':
            data = data.sort_values('day',ascending=False).iloc[:20,:]
        elif method=='BelowNegative5':
            data = data.sort_values('day',ascending=True).iloc[:20,:]
        elif method=='WeekAbovePositive10':
            data = data.sort_values('week',ascending=False).iloc[:20,:]
        elif method=='WeekBelowNegative10':
            data = data.sort_values('week',ascending=True).iloc[:20,:]
        elif method=='MonthAbovePositive20':
            data = data.sort_values('month',ascending=False).iloc[:20,:]
    else:
        if method=='AbovePositive5':
            data = data.sort_values('day',ascending=False)
        elif method=='BelowNegative5':
            data = data.sort_values('day',ascending=True)
        elif method=='WeekAbovePositive10':
            data = data.sort_values('week',ascending=False)
        elif method=='WeekBelowNegative10':
            data = data.sort_values('week',ascending=True)
        elif method=='MonthAbovePositive20':
            data = data.sort_values('month',ascending=False)
    data=json.loads(data.to_json(orient='records'))
    return data


def get_top_twitter(which_day,num):
    which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
    with open(f'./UIData/twitter/{which_day}_{num}.json')as f:
        file = json.load(f)
        key = file[0]
        twitter = file[1:]
    return key,twitter
def get_hot_twitter(which_day):
    which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
    with open(f'./UIData/twitter/FundyLongShort+{which_day}.json')as f:
        file1 = json.load(f)
    with open(f'./UIData/twitter/SmallCapLS+{which_day}.json')as f:
        file2 = json.load(f)
    with open(f'./UIData/twitter/ShortSightedCap+{which_day}.json')as f:
        file3 = json.load(f)
    return file1,file2,file3
        
@app.route("/log/create-entry", methods=["POST"])
def create_entry():
    time=dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
    req = request.get_json()
    print(req)
    with open(f'./schema/Info.json', 'r') as json_file:
        data = json.load(json_file)
    int = 0
    try:
        while str(int) in data[user].keys():
            int = int + 1
    except:
        return render_template('login.html')
    data[user].update({int: {"date": "",
                             "pf": "",
                             "kw": "",
                             "clc": {"url": req['url'], "title" : req['title'], "tab": req['tab'],
                                     'click_time':time
                                     }}})
    with open(f'./schema/Info.json', 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()
    res = make_response(jsonify({"message": "OK"}), 200)

    return res

    
if __name__ == "__main__":
    app.run()

    