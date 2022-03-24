import re

with open('cache/kyonh.txt') as f:
    kyonh2descr = dict(line.rstrip('\n').split('\t')[::-1] for line in f)

with open('cache/tshet.txt') as f:
    descr2tshet = dict(line.rstrip('\n').split('\t') for line in f)


FIXES = {
    '曉開齊上': (
        (None, '匣開齊上'),
    ),
    '羣開佳上': (
        ('箉', '定開佳上'),
        (None, '見合佳上'),
    ),
}


def convert(ch, roman_kyonh):
    descr = kyonh2descr[roman_kyonh]
    for chs, fix in FIXES.get(descr, ()):
        if chs is None or ch in chs:
            descr = fix
            break
    return descr2tshet[descr]


def do(fin, fout, ferr):
    # header
    for line in fin:
        line = line.rstrip('\n')

        if line == '...':
            print(line, file=fout)
            break

        if line.startswith('version:'):
            line = re.sub('''(["']?)$''', r'-fixes\1', line, 1)

        line = line.replace('kyonh', 'tshet')
        print(line, file=fout)

    # data
    for line in fin:
        line = line.rstrip('\n')

        if not line:
            print(file=fout)
            continue

        word, romans_str, *extras = line.split('\t')
        romans = romans_str.split(' ')
        assert len(word) == len(romans)

        try:

            romans = ' '.join(convert(c, roman)
                              for c, roman in zip(word, romans))
            print(word, romans, *extras, sep='\t', file=fout)
        except KeyError:
            for c, roman in zip(word, romans):
                if roman not in kyonh2descr:
                    print(roman, c, file=ferr)


with open('cache/unhandled2.txt', 'w') as ferr:
    with open('../rime-kyonh/kyonh.dict.yaml') as fin, open('tshet.dict.yaml', 'w') as fout:
        do(fin, fout, ferr)
    with open('../rime-kyonh/kyonh.words.dict.yaml') as fin, open('tshet.words.dict.yaml', 'w') as fout:
        do(fin, fout, ferr)
