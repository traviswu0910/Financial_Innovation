from Module_MetaClass import Clean
import re
import json
import pandas as pd

co_list = pd.read_json('./Schema/Reference/InfoCodeToFullName.json').InfoCode.values.tolist()
def not_redundant_int(x):
    '''
    有些數字在做文字探勘時要去掉，但如果這些數字是公司的infocode則先不去掉
    '''
    try:
        x=int(x)
        if x not in co_list:
            return False
        else:return True
    except:return True
    #return False 代表是要被清掉的詞
    
class Clean(Clean):
    def Capitalize(self):
        self.Text = self.Text.upper()
        return self

    def Separate(self, gram=1):
        parts = self.Text.split(" ")
        self.Text = []
        for i in range(len(parts) + 1 - gram):
            text = ""
            for j in range(gram):
                if j < gram and j != 0:
                    text = text + " " + str(parts[i + j])
                else:
                    text = text + str(parts[i + j])
            self.Text.append(text)
        return self

    def DeletePunctuation(self
                          , punctuation=["'S", "S'",'‘S','’S',',', '\.', '-', '"', "'",":",";",'!','‘','\$','@','’']
                          ):
        mid = self.Text
        for puncs in punctuation:
            mid = re.sub(puncs, '', mid)
        resultwords = re.split(" \W+ ", mid)
        self.Text = " ".join(resultwords)
        return (self)
    

    def DeleteRedundant(self):
        words=['A', 'THE', 'AN', 'TO', 'AND', 'OR', 'NOT','HE','HE','SHE','HIS','HER','THEM','THEY','BACK',
               'WANT','RIGHT','LEFT','WITHOUT','WITH','THEM','OF','AS','IN','MORE','FOR','ARE','IS','NEW','WILL','BE','AFTER',
               'WANTS', 'KNOW', 'HE', 'HISTORY', 'NAMES', 'TOO', 'RUN', 'NEEDS', 'WEEK', 'ANOTHER', 'GETTING', 'ON','BUT','COULD',
               'OUT','AT','THAN','HAVE','BY','WHAT','CAN','CANT','NOW','OVER','IT','ABOUT','MAY','HAS','HAVE','THEIR','QUARTER','DUE','UP','ITS',
               'YOU','YOUR','ENEN','WHY','HOW','THAT','THERE','THESE','NO','BEFORE','DO','DID','DONE','DOING','DONT','WAS','WERE',
               'LOOK','DON’T','ALL','INTO','ONTO','AROUND','TOWARDS','FROM','REVIEW','EUROPE','NORTH','GOVERNMENT','EXPERT',''
               'LEAD', 'NEED', 'GOES', 'BEHIND', 'GROUP', 'NEAR', 'WORKING', 'METOO', 'IF', 'GETS', 'GO', 'COMES', 'WHEN', 'THERE', 
               'PUT', 'USE', 'GOING', 'TALKS', 'WE', 'THEY', 'LIKELY', 'I', 'MONTH', 'OUR', 'PLAY', 'OWN', 'MY', 'MAKES', 'AD', 
               'AWAY', 'OFF', 'MUCH', 'LIVE', 'TV', 'NEARLY', 'DURING', 'BRING', 'PLAN', 'YIELD', 'WIN', 'FINALLY', 'TRY', 'AMONG', 
               'TAKING', 'WHERE', 'MADE', 'BUILD', 'TIES', 'HERE', 'THINK', 'YET', 'BOYS', 'RULES', 'NEXT', 'LESS', 'PART',
               'LEAVES', 'ASKS', 'NEWS', 'JUST', 'LOOKS', 'BEYOND', 'LATEST', 'KEY', 'MOVE', 'THIS', 'FINDS', 'THOSE', 'LITTLE', 
               'LIKE', 'BEEN', 'TODAY', 'NOTHING', 'HER', 'ALMOST', 'HAD', 'COMING', 'EDGES', 'FIRST', 'READ', 'AGAIN', 'DAY', 
               'WEAK', 'BETTER', 'LET', 'BETWEEN', 'GROWING', 'TAKE', 'LEARN', 'MONTHS', 'BEING', 'YEAR', 'MINUTES', 
               'RUNNING', 'RECORD', 'QUESTION', 'VS', 'WOULD', 'TOP', 'WAY', 'MANY', 'PEOPLE', 'HIS', 'EASY', 'SOME', 
               'ACROSS', 'DRIVE','WANT','NEED','GET','TALK','MAKE','US','CHINA','BIG','YORK','WORLD','MILLION',
               'WHITE','MARKET','MARKETS','TIME','AMERICA','UK','MAN','WOMAN','MEN','WOMEN','CAN’T','TWO','AMID','KEEP','END','HELP',
               'YEARS','LIFE','HIT','YES','ASK','WHICH','WHO','HOME','SAYS','SAY','STOCK','STOCKS','GOOD','PUSH','ONE','SUPER','INVESTORS',
               'INVESTOR','POWER','CITY','CALL','CALLS','BILLION','MILLION','WATCH','LOVE','TOO','JOURNAL','WALL','STREET','SHOW','SHOWS',
               'STATE','STATES','TUESDAY','STRONG','SO','MOST','DECADE','UNDER','REPORT','ECONOMY','UNIT'
               
               ]
        resultwords = [word for word in re.split("\s+", self.Text) if word.upper() not in words and len(word)>1 and not_redundant_int(word)]
        self.Text = " ".join(resultwords)
        return (self)
