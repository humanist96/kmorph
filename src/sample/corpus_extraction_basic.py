# -*- coding: utf-8 -*-

from natto import MeCab
import collections


_morpheme_type = ['NNG', 'NNP']
_escape_pattern = ['\n']
_nm = MeCab()


def filter_by_type(text):
    words = []
    for term_info in str(_nm.parse(text)).split('\n'):
        _term_info = term_info.split('\t')
        if len(_term_info) < 2:
            continue
        surface = _term_info[0]
        analysis = _term_info[1].split(',')
        if analysis[0] in _morpheme_type:
            words.append(surface)
    return words


def generate_corpus(data_path):
    _corpus = []
    fp = open(data_path, 'r')
    for line in fp.readlines():
        if line not in _escape_pattern:
            terms = filter_by_type(line)
            _corpus.append(terms)
    return _corpus


def term_frequency(_corpus):
    _terms = []
    for words in _corpus:
        _terms.extend(words)
    return sorted(collections.Counter(_terms).items(), key=lambda x: x[1], reverse=True)


def display_list(x_list):
    for x in x_list:
        print(x)


if __name__ == '__main__':
    corpus = generate_corpus('./news.txt')
    term_frequency = term_frequency(corpus)
    print('- corpus (noun) - ')
    display_list(corpus)
    print('- term frequency best 10 - ')
    display_list(term_frequency[0:10])


