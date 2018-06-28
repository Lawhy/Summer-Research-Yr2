import re


def check_chi(s):
    f = open(s + ".txt", 'r', encoding='UTF-8')
    chi = r'^[\u4E00-\u9FA5]+$'
    pa = re.compile(chi)
    ok = True
    lines = [line.rstrip('\n') for line in f]
    fst = True
    count = 0
    for l in lines:
        if not re.findall(pa, l) and not fst:
            print(l)
            ok = False
        fst = False
        count += 1
    if ok:
        print('OK!')
        print(count)
    f.close()


def check_eng(s):
    f = open(s + ".txt", 'r', encoding='UTF-8')
    eng = r'^[A-Za-z]+$'
    pa = re.compile(eng)
    ok = True
    lines = [line.rstrip('\n') for line in f]
    fst = True
    count = 0
    for l in lines:
        l = l.replace('\'', '')
        if not re.findall(pa, l) and not fst:
            print(l)
            ok = False
        fst = False
        count += 1
    if ok:
        print('OK!')
        print(count)
    f.close()

def check_all(s):
    f = open(s + ".txt", 'r', encoding='UTF-8')
    ec = r'^[A-Za-z]+\t[\u4E00-\u9FA5]+$'
    pa = re.compile(ec)
    ok = True
    lines = [line.rstrip('\n') for line in f]
    fst = True
    count = 0
    for l in lines:
        l = l.replace('\'', '')
        if not re.findall(pa, l) and not fst:
            print(l)
            ok = False
        fst = False
        count += 1
    if ok:
        print('OK!')
        print(count)
    f.close()


check_chi('en2chi_tra_chi')
check_eng('en2chi_tra_eng')
check_all('en2chi_tra')




