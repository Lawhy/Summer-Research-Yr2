import re

uffe8 = '￨'  # the separator used in word features

def check_dup(file):
    with open(file, 'r', encoding='UTF-8') as inp:
        lines = inp.readlines()
    distinct = set()
    for line in lines:
        distinct.add(line)
    if len(distinct) == len(lines):
        print('No dup!')
    else:
        # for dist in distinct:
        #     count = 0
        #     for word in lines:
        #         if dist == word:
        #             count += 1
        #         if count > 1:
        #             print(dist)
        #             break
        print(len(lines) - len(distinct))


def lower_everything(eng_file):
    with open(eng_file, 'r', encoding='UTF-8-sig') as ip:
        lines = [line.lower() for line in ip.readlines()]
        print(lines)
    with open('./baseline/' + eng_file, 'w+', encoding='UTF-8') as output:
        output.writelines(lines)


lower_everything('en2chi_tst_eng.txt')
