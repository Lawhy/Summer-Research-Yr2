import re
import math


def removeDup(s):
    f = open(s + '.txt', 'r', encoding='UTF-8')
    f_out = open(s + '_out.txt', 'w+', encoding='UTF-8')
    f_dup = open(s + '_dup.txt', 'w+', encoding='UTF-8')
    clean_list = []
    count_dup = 0
    for line in f:
        if line in clean_list:
            count_dup += 1
            f_dup.write(line)
            print(line)
            continue
        clean_list.append(line)
    f_out.writelines(clean_list)
    print(str(count_dup) + ' duplicates')
    f.close()
    f_out.close()
    f_dup.close()


def separate(s):
    f = open(s + '.txt', 'r', encoding='UTF-8-sig')
    f_chi = open(s + '_chi.txt', 'w+', encoding='UTF-8')
    f_eng = open(s + '_eng.txt', 'w+', encoding='UTF-8')
    f_rest = open(s + '_res.txt', 'w+', encoding='UTF-8')
    ec = r'^([A-Z].*[a-z])\t([\u4E00-\u9FA5]+\n)$'
    pa = re.compile(ec)
    eng = []
    chi = []
    count = 0
    for line in f:
        wp = re.findall(pa, line)
        if not wp:
            print(line)
            f_rest.write(line)
            continue
        count += 1
        eng.append(wp[0][0] + '\n')
        chi.append(wp[0][1])
    f_eng.writelines(eng)
    f_chi.writelines(chi)

    f.close()
    f_chi.close()
    f_eng.close()
    f_rest.close()


def divide(s):
    f_tra = open(s + '_tra.txt', 'w+', encoding='UTF-8-sig')
    f_eva = open(s + '_eva.txt', 'w+', encoding='UTF-8')
    f_tst = open(s + '_tst.txt', 'w+', encoding='UTF-8')
    n = len(open(s + '.txt', 'r', encoding='UTF-8').readlines())
    f = open(s + '.txt', 'r', encoding='UTF-8')
    print(n)
    n_tra = math.floor(n * 0.8)
    print(n_tra)
    n_eva = math.floor(n * 0.1)
    print(n_eva)
    count = 0
    for line in f:
        count += 1
        if count <= n_tra:
            f_tra.write(line)
        elif (count - n_tra) <= n_eva:
            f_eva.write(line)
        else:
            f_tst.write(line)
    f.close()
    f_tra.close()
    f_eva.close()
    f_tst.close()


# def count_chi(s):
#     f = open(s + '.txt', 'r', encoding='UTF-8')
#     chi_set = set()
#     for word in f:
#         word = word.replace('\n', '')
#         for char in word:
#             chi_set.add(char)
#     print(len(chi_set))
#     f.close()
#     # with open(s + '_char.txt', 'w+', encoding='UTF-8') as out:
#     #     out.writelines('\n'.join(chi_set))
#     return chi_set


def chi_char(s):
    chi_set = set()
    chi = r'[\u4E00-\u9FA5]'
    with open(s + '.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    for line in lines:
        for char in line:
            if bool(re.match(chi, char)):
                chi_set.add(char)
    with open('chi_char.txt', 'w+', encoding='UTF-8') as output:
        for char in chi_set:
            output.write(char)
    return chi_set



# chi_set = count_chi('en2chi_tra_chi')
# chi_set_ipa = count_chi_IPA('IPA_chi')
# chi_rest = set()
# chi_exc = set()
#
# print(bool('\t' in chi_set))
#
# for chi in chi_set:
#     if chi not in chi_set_ipa:
#         chi_rest.add(chi)
#         # print(chi)
# for chi in chi_set_ipa:
#     if chi not in chi_set:
#         chi_exc.add(chi)
#         # print(chi)chi_set_ipa = count_chi_IPA('IPA_chi')
# chi_rest = set()
# chi_exc = set()
#
# print(bool('\t' in chi_set))
#
# for chi in chi_set:
#     if chi not in chi_set_ipa:
#         chi_rest.add(chi)
#         # print(chi)
# for chi in chi_set_ipa:
#     if chi not in chi_set:
#         chi_exc.add(chi)
#         # print(chi)

# with open('rest.txt', 'w+', encoding='UTF-8') as m:
#     m.writelines(chi_rest)










