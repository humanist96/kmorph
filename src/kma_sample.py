# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/workspace/my_bigdata/kmorph/src/kma");
import kma_api as a

if __name__ == '__main__':
    
    ret=''

    me, df=a.run_ma("코스콤(Koscom)은 여의도에 위치하고 있다.", "./stopword.txt", 2)
    print(" -- morpheme analzyer info --")
    print(me)
    print(" -- all info of morpheme analzyer  --")
    print(df)
    print(" -- all morphemes and POS --")
    ret=a.get_all_morph(df)
    print(ret)
    print(" -- noun morphemes and POS --")
    ret=a.get_noun_morph(df)
    print(ret)
    print(" -- noun morphemes and freq --")
    ret=a.get_noun_term_freq(df)
    print(ret)
