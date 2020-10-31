# Extract Top-n dictionary from bilingual alignment

This is the python code to extract the top-n dictionary from the bilingual alignment information(Pharaoh format) which is extracted from fastalign or GIZA++.

---


# Toy test

input :  
"./test_data/test.src" (50 Korean sentences)  
"./test_data/test.tgt" (50 English sentences)  
"./test_data/test.src-tgt.align" (50 Korean-English alignment from GIZA++)

output :  

Top-n dictionary

'''
In [2]: from Test import ExtractDict

In [3]: extractdict = ExtractDict("./test_data/test.src", "./test_data/test.tgt", "./test_data/test.src-tgt.align", N=5, n_best=3)

In [4]: extractdict.topNdict
Out[4]:
defaultdict(None,
            {'.': ['.'],
             '이': ['this', 'were', 'are'],
             '을': ['for', 'with'],
             '에': ['on', 'in'],
             '가': ['are', 'is']})

In [5]: extractdict1 = ExtractDict("./test_data/test.src", "./test_data/test.tgt", "./test_data/test.src-tgt.align", N=30, n_best=1)

In [6]: extractdict1.topNdict
Out[6]:
defaultdict(None,
            {'.': ['.'],
             '이': ['this'],
             '을': ['for'],
             '에': ['on'],
             '가': ['are'],
             '의': ['of'],
             '것': ['that'],
             '는': ['the'],
             '은': ['the'],
             ',': ['and'],
             '으로': ['due'],
             '등': ['as'],
             '했다': ['made'],
             '들': ['are'],
             '과': ['and'],
             '고': ['that'],
             '“': ['said'],
             '인': [','],
             '에서': ['in'],
             '로': ['as'],
             '하고': ['and'],
             '”': ['&quot;'],
             '하는': ['that'],
             '있다': ['is'],
             '다': ['is'],
             '‘': ['&quot;'],
             '’': ['&quot;'],
             '해': ['will']})
'''

