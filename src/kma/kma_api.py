# -*- coding: utf-8 -*-
# Copyright (C) 2018.02.09 kyung seok jeong <humanist96@koscom.co.kr>
from __future__ import absolute_import, unicode_literals
from natto import MeCab
import pandas as pd
import collections
import re
import datrie
import string


def load_stopword(fpath):
    """
    Return the trie object of stopword dictionary
    - input : stopword file path
    - output : trie instance
    """
    _escape_pattern = ['\n']
    
    try:
        trie=datrie.Trie(ranges=[(u'\u0000', u'\uFFFF')])

        with open(fpath, "rb", 0) as f:
            for word in f.readlines():
                word=word.decode("utf-8").rstrip()           
                trie[word] = True
    except Exception as e:
        print("[load_storpwod] messages of error :", e)
        return ''
    
    return trie


def is_stopword(morpheme, trie):
    """
    Returns the presence or absence of stopword in stopword dictionary.
    - input : morpheme string, trie instance
    - output : boolean (Ture, False)
    """
    if morpheme in trie:
        return True
    
    return False


def run_ma(text, stop_path='', nBest=1):
    """
    Returns the dataframe of all Information of morpheme analyzer.
    - input : string, {stopword file path}, {nbest number}
    - output : dataframe
    """
    options=r'-F%m,%f[0],%f[1],%f[2],%f[3],%f[4],%f[5],%f[6],%f[7]\n'
    options+=" -N"+str(nBest)
    
    stopword_flag=False
    
    if stop_path != '':
        stopword_flag=True
    try:   
        _me=MeCab(options)

        _df = pd.DataFrame(None, columns=['surface', 'tag', 'meaning_class', 'final_consonant', 
                                         'reading', 'type', 'first_tag', 'final_tag','expression'])

        if stopword_flag:
            trie=load_stopword(stop_path)

        i=0
        for term_str in str(_me.parse(text)).split('\n'):
            term_list = re.split(',', term_str)

            if stopword_flag == True and is_stopword(term_list[0], trie):
                continue
            if len(term_list) < 2:
                continue

            _df.loc[i]=term_list   
            i+=1
    except Exception as e:
        print("[run_ma] messages of error : ", e)
        
    return _me, _df


def get_all_morph(df):
    """
    Returns all morphemes and Part-of-Speech.
    - input : dataframe
    - output : string
    """
    ret=''
    for index, row in df.iterrows():      
        if row['type'] == 'Inflect' or row['type'] == 'Compound':
            tag=row['expression']
            ret+=tag.replace('+',' ').replace("/*", '')+" "
        else:
            tag=row['tag']
            ret+=row['surface']+"/"+tag+" "        
    ret=ret.rstrip()
    ret=ret+"\n"
    
    return(ret)


def get_noun_morph(df, option='N'):
    """
    Returns noun morphemes and Part-of-Speech.
    - input : dataframe, {option : compound noun decomposition flag, default : N}
    - output : string
    """
    _noun_type = ['NNG', 'NNP']
    ret=''
    
    for index, row in df.iterrows():
        if row['tag'] in _noun_type:
            if row['type'] == 'Compound' and option != 'N':
                tag=row['expression']
                ret+=tag.replace('+',' ').replace("/*", '')+" "
            else:
                ret+=row['surface']+"/"+row['tag']+" " 
    ret=ret.rstrip()
    ret=ret+"\n"
    
    return(ret)


def get_noun_term_freq(df, option='N'):
    """
    Returns noun morphemes and freqeuncy
    - input : dataframe, {option : compound noun decomposition flag, default : N}
    - output : list of tuples(morpheme, frequency)
    """
    _noun_type = ['NNG', 'NNP']
    _terms = []
    
    for index, row in df.iterrows():
        if row['tag'] in _noun_type:
            if row['type'] == 'Compound' and option != 'N':
                tag=row['expression']
                _terms.extend(re.split(' ', tag.replace('+',' ').replace("/*", '')))
            else:
                _terms.append(row['surface'])
                
    return sorted(collections.Counter(_terms).items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    ret=''
    me, df=run_ma("어떤 기자가 대한민국 형태소분석기는 한글을 잘 분석할지 물었다?", "./stopword.txt")
    print(" -- morpheme analzyer info --")
    print(me)
    print(" -- all info of morpheme analzyer  --")
    print(df)
    print(" -- all morphemes and POS --")
    ret=get_all_morph(df)
    print(ret)
    print(" -- noun morphemes and POS --")
    ret=get_noun_morph(df)
    print(ret)
    print(" -- noun morphemes and freq --")
    print(get_noun_term_freq(df))
