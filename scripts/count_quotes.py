text=open('scripts/w33_universal_search.py','r',encoding='utf-8').read()
print('count', text.count('"""'))
# split on "\n" rather than splitlines(): the latter treats formfeed and vertical tab as
# line breaks, shifting every reported line number past such a byte (Pass 4929).
for i,line in enumerate(text.split(chr(10)),1):
    if '"""' in line:
        print(i, line)
