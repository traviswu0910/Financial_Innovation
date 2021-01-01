# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:15:34 2020
@author: USER
"""
import pandas as pd
import html

class Clean:
    '''
    Type:
        Text: the text which need to be clean. (str)
    Description:
        Clean the content in the text.
    '''
    def __init__(self,Text):
        self.Text=Text



    def Capitalize(self):
        '''
        Description:
            Make the letters in self.Text are capital.(str)
        '''

        return(self)

    def Separate(self,gram=1):
        '''
        Type:
            gram: the number of grams for each entry.(int)
        Description:
            Separate self.Text by n-gram (list with str)
        '''
        return(self)

    def DeletePunctuation(self
            ,Punctuation=[',','.','-','"',"'","'S","S'"]
        ):
        '''
        Type:
            Punctuation: the list of punctuations(list with str)
        Description:
            Cancel the punctuations in self.Text(str)
        '''
        return(self)

    def DeleteRedundant(self
            ,Words=['A','THE','AN','TO','AND','OR','NOT']
        ):
        '''
        Type:
            Words: the list of redundant words(list with str)
        Description:
            Cancel the redundants in self.Text(str)
        '''
        return(self)
    
    def Substitute(self,Oldletter,Newletter):
        '''
        Type:
            Oldletter: The letter in the text to be substituted (str)
            Newletter: The updated letter(str)
        Description:
            Substitute all letters(Oldletter) in the text by Newletter(str)
        '''
        return(self)
        
    def Close(self):
        '''
        Description:
            End the clean procedure and return the result after cleaning
        '''
        return(self.Text)

'''
Description:
    In: Clean('I am Text).Capitalize().Close()
    Out: 'I AM TEXT'
    
    In: Clean('I am Text').Separate(gram=1).Close()
    Out: ['I','am','Text']
    
    In: Clean('I am Text').Separate(gram=1).Close()
    Out:['I am','am Text']
    
    In: Clean('I am Text, a Type's man').DeletePunctuation(Punctuation=[",","'s"]).Close()
    Out:'I am Text a Type man'
    
    In: Clean('I am a Text').DeleteRedunduant(Words=["am","a"]).Close()
    Out: 'I Text'
    
    In: Clean('I am a Text').Substitute(Oldletter='Text',Newletter='Lion').Close()
    Out: 'I am a Lion'
'''

class Crawler:
    '''
    Type:
        Name: The name of the web. (str)
        Source: The source(url) of the web(str)
    Description:
        Crawler the contents of the web
    '''
    RawData=''
    CrawlerTime={'Start':19000101000000,'End':21001231235959}
    ParsedData={}
    
    def __init__(self,Name,Source):
        self.Name=Name
        self.Source=Source
        
    
    def CrawlerRawData(self):
        '''
        Description:
            Crawler the raw data in the target web and then deposit in the 
            property, self.RawData(str)
        '''
        return(self)
    
    def __RecordCrawlerTime(self):
        '''
        Description:
            Record the starting and ending time(yyyymmddhhMMss, int) about 
            crawlering and deposit in the property, self.CrawlerTime 
        '''
    
    def ParseRawData(self):
        '''
        Description:
            Parse the rawdata and deposit in the property, self.ParseData whose
            keys are tags and values are contents. 
            See https://docs.python.org/3/library/html.parser.html
        '''
    
    def Close(self):
        return(self.ParsedData)


# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:15:34 2020
@author: USER
"""

import pandas as pd
import html

class Clean:
    '''
    Type:
        Text: the text which need to be clean. (str)
    Description:
        Clean the content in the text.
    '''
    def __init__(self,Text):
        self.Text=Text



    def Capitalize(self):
        '''
        Description:
            Make the letters in self.Text are capital.(str)
        '''

        return(self)

    def Separate(self,gram=1):
        '''
        Type:
            gram: the number of grams for each entry.(int)
        Description:
            Separate self.Text by n-gram (list with str)
        '''
        return(self)

    def DeletePunctuation(self
            ,Punctuation=[',','.','-','"',"'","'S","S'"]
        ):
        '''
        Type:
            Punctuation: the list of punctuations(list with str)
        Description:
            Cancel the punctuations in self.Text(str)
        '''
        return(self)

    def DeleteRedundant(self
            ,Words=['A','THE','AN','TO','AND','OR','NOT']
        ):
        '''
        Type:
            Words: the list of redundant words(list with str)
        Description:
            Cancel the redundants in self.Text(str)
        '''
        return(self)
    
    def Substitute(self,Oldletter,Newletter):
        '''
        Type:
            Oldletter: The letter in the text to be substituted (str)
            Newletter: The updated letter(str)
        Description:
            Substitute all letters(Oldletter) in the text by Newletter(str)
        '''
        return(self)
        
    def Close(self):
        '''
        Description:
            End the clean procedure and return the result after cleaning
        '''
        return(self.Text)

'''
Description:
    In: Clean('I am Text).Capitalize().Close()
    Out: 'I AM TEXT'
    
    In: Clean('I am Text').Separate(gram=1).Close()
    Out: ['I','am','Text']
    
    In: Clean('I am Text').Separate(gram=1).Close()
    Out:['I am','am Text']
    
    In: Clean('I am Text, a Type's man').DeletePunctuation(Punctuation=[",","'s"]).Close()
    Out:'I am Text a Type man'
    
    In: Clean('I am a Text').DeleteRedunduant(Words=["am","a"]).Close()
    Out: 'I Text'
    
    In: Clean('I am a Text').Substitute(Oldletter='Text',Newletter='Lion').Close()
    Out: 'I am a Lion'
'''

class Crawler:
    '''
    Type:
        Name: The name of the web. (str)
        Source: The source(url) of the web(str)
    Description:
        Crawler the contents of the web
    '''
    RawData=''
    CrawlerTime={'Start':19000101000000,'End':21001231235959}
    ParsedData=[{}]
    
    def __init__(self,Name,Source):
        self.Name=Name
        self.Source=Source
        
    
    def CrawlerRawData(self):
        '''
        Description:
            Crawler the raw data in the target web and then deposit in the 
            property, self.RawData(str)
        '''
        return(self)
    
    def __RecordCrawlerTime(self):
        '''
        Description:
            Record the starting and ending time(yyyymmddhhMMss, int) about 
            crawlering and deposit in the property, self.CrawlerTime 
        '''
    
    def ParseRawData(self):
        '''
        Description:
            Parse the rawdata and deposit in the property, self.ParseData whose
            keys are tags and values are contents. 
            See https://docs.python.org/3/library/html.parser.html
        '''
    
    def Close(self):
        return(self.ParsedData)

