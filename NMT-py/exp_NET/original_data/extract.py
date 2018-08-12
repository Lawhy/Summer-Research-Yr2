import re

dic = {
    "64": 'tra',
    "16": 'dev',
    "20": 'tst'
}


def extract(file, lan, tra_dev_tst):
    with open(file, 'r', encoding='UTF-8') as inp:
        lines = inp.readlines()

    ens = []
    others = []
    count = 0

    for line in lines:
        wp = re.sub(r'\t[0-9]+', '', line)  # remove weird numbers
        wp = re.findall(r'(.+)\t(.+)', wp)

        if not wp:
            continue

        wp = wp[0]
        assert len(wp) == 2

        en = wp[0].replace('\n', '')
        other = wp[1].replace('\n', '').replace(' ', '')

        if not re.match(r'^[\'\w]+$', en):
            count += 1
            continue
        if not re.match(r'^[\'\w]+$', other):
            count += 1
            continue

        en = ' '.join(en)
        ens.append(en)
        other = ' '.join(other)
        others.append(other)

    print(count)

    with open('en_' + tra_dev_tst + '.txt', 'w+', encoding='UTF-8') as eng:
        for e in ens:
            eng.write(e + '\n')

    with open(lan + '_' + tra_dev_tst + '.txt', 'w+', encoding='UTF-8') as otr:
        for o in others:
            otr.write(o + '\n')


for portion in dic.keys():
    extract('wd_russian_' + portion, 'ru', dic[portion])
