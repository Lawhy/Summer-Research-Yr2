import re
import random
out = '_out.txt'
space = '_space.txt'
sup = '_sup.txt'
f0 = open('People' + out, 'r', encoding='UTF-8')
f1 = open('People' + sup, 'r', encoding='UTF-8')
f2 = open('People' + space, 'r', encoding='UTF-8')
eng_chi = r'^([A-Z].*[a-z])\t([\u4E00-\u9FA5]+)'
pa = re.compile(eng_chi)
count = 0
long_list = []
for line in f0:
    long_list.append(line)
    count += 1
print(count)
for line in f1:
    count += 1
    long_list.append(line)
print(count)
for line in f2:
    count += 1
    long_list.append(line)
print(count)

f0.close()
f1.close()
f2.close()
print(count)

random.shuffle(long_list)
random.shuffle(long_list)
random.shuffle(long_list)

f_all = open('All.txt', 'w+', encoding='UTF-8')
f_chi = open('All_chi.txt', 'w+', encoding='UTF-8')
f_eng = open('All_eng.txt', 'w+', encoding='UTF-8')
f_res = open('Rest.txt', 'w+', encoding='UTF-8')
for line in long_list:
    wp = re.findall(pa, line)
    if not wp:
        print(line)
        f_res.writelines(line)
    else:
        eng = wp[0][0]
        chi = wp[0][1]
        f_all.writelines(line)
        f_chi.writelines(chi + '\n')
        f_eng.writelines(eng + '\n')
f_all.close()
f_chi.close()
f_eng.close()
f_res.close()
