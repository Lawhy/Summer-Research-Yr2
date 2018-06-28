import re

def deleteIrr(s):
    # f_chi = open(s + '_chi.txt', 'w+', encoding='UTF-8')
    f_gen = open(s + '_gen.txt', 'w+', encoding='UTF-8')
    f_out = open(s + '_out.txt', 'w+', encoding='UTF-8')
    f_sup = open(s + '_sup.txt', 'w+', encoding='UTF-8')
    f_pro = open(s + '_pro.txt', 'w+', encoding='UTF-8')
    f_space = open(s + '_space.txt', 'w+', encoding='UTF-8')
    s = s + '.txt'
    f = open(s, 'r+', encoding='UTF-8')

    eng_chi = r'([A-Z].*[a-z])\t\w.*\t([\u4E00-\u9FA5]+).*$'
    ec_gen = r'([A-Z].*[a-z])\t\w.*\t([\u4E00-\u9FA5].*)$'
    pa = re.compile(eng_chi)

    count = 0
    count_spa = 0
    count_gender = 0
    count_sub = 0
    count_error = 0
    for line in f:
        if '(女名)' in line and ';' in line:
            pa_gen = re.compile(ec_gen)
            ec = re.findall(pa_gen, line)

            eng = ec[0][0]
            chi = ec[0][1]

            f_gen.writelines(eng + '\t' + chi + '\n')
            count_gender += 1
            print(str(ec) + str(count_gender))
            continue
        # print(ec)
        ec = re.findall(pa, line)
        if not ec == []:
            eng = ec[0][0]
            chi = ec[0][1]

            if '′' in eng:
                eng = eng.replace('<sup>′</sup>', '\'')
                f_sup.writelines(eng + '\t' + chi + '\n')
                count_sub += 1
                continue
            if ' ' in eng:
                f_space.writelines(eng + '\t' + chi + '\n')
                count_spa += 1
                continue

            # print(eng + '\t' + chi)
            f_out.writelines(eng + '\t' + chi + '\n')
            # f_chi.writelines(chi + '\n')
            count += 1
        else:
            # print(str(count) + 'th line has a problem: ' + str(ec))
            f_pro.writelines(line)
            count_error += 1
    print("There are " + str(count) + " words")
    print("There are " + str(count_gender) + " neutral words")
    print("There are " + str(count_sub) + " sub words")
    print("There are " + str(count_error) + " problems")
    print("There are " + str(count_spa) + " words with space")
    print("There are " + str(count + count_gender + count_spa + count_sub + count_error) + " words in total")
    f.close()
    f_out.close()
    f_gen.close()
    f_pro.close()
    f_space.close()
deleteIrr("People")