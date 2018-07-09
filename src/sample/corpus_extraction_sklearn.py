# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from natto import MeCab


_morpheme_type = ['NNG', 'NNP']
_escape_pattern = ['\n']
_nm = MeCab()


def filter_by_type(text):
    terms = []
    for term_info in str(_nm.parse(text)).split('\n'):
        _term_info = term_info.split('\t')
        if len(_term_info) < 2:
            continue
        surface = _term_info[0]
        analysis = _term_info[1].split(',')
        if analysis[0] in _morpheme_type:
            terms.append(surface)
    return terms


def generate_corpus2(data_path):
    _corpus = []
    fp = open(data_path, 'r')
    for line in fp.readlines():
        if line not in _escape_pattern:
            terms = filter_by_type(line)
            _corpus.append(' '.join(terms))
    return _corpus


corpus = generate_corpus2('news.txt')
print('corpus : ', corpus)
_cv = CountVectorizer()
word_matrix = _cv.fit_transform(corpus)

index = 0
for word_vector in word_matrix.toarray():
    print('[', corpus[index], '] \n: ', word_vector)
    index += 1
