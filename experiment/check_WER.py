
import re


def exp_result(filename):
    chi = r'[\u4E00-\u9FA5]'
    pa = re.compile(chi)

    with open(filename + '.txt', 'r', encoding='UTF-8-sig') as f:
        lines = f.readlines()

    with open('en2chi_tst.txt', 'r', encoding='UTF-8-sig') as tst:
        answers = tst.readlines()

    assert len(lines) == len(answers)

    count_chars = 0
    count_CER = 0
    count_WER = 0

    for i in range(len(lines)):
        predict = re.findall(pa, lines[i])
        answer = re.findall(pa, answers[i])
        # count CER
        if len(predict) >= len(answer):
            for j in range(len(answer)):
                if answer[j] == predict[j]:
                  count_CER += 1
        else:
            for j in range(len(predict)):
                if answer[j] == predict[j]:
                    count_CER += 1
        count_chars += len(predict)
        # count WER
        if predict == answer:
            count_WER += 1

        print(predict + ['|'] + answer)

    w_acc = count_WER/len(lines)
    c_acc = count_CER/count_chars
    print('WER: ' + str(1 - w_acc))
    print('CER: ' + str(1 - c_acc))
    return {
        'WER': 1 - w_acc,
        'CER': 1 - c_acc,
    }


def extract(filename):
    chi = r'[\u4E00-\u9FA5]'
    eng = r'[A-Za-z\']'
    pa_chi = re.compile(chi)
    pa_eng = re.compile(eng)
    with open(filename + '.txt', 'r', encoding='UTF-8-sig') as inp:
        lines = inp.readlines()
    wschi = []
    wseng = []
    for wp in lines:
        wchi = re.findall(pa_chi, wp)
        weng = re.findall(pa_eng, wp)
        wchi = ' '.join(wchi)
        weng = ' '.join(weng)
        wschi.append(wchi)
        wseng.append(weng)
    assert len(wschi) == len(wseng)
    with open(filename + '_chi.txt', 'w+', encoding='UTF-8') as opchi:
        for wchi in wschi:
            opchi.write(wchi + '\n')
    with open(filename + '_eng.txt', 'w+', encoding='UTF-8') as openg:
        for weng in wseng:
            openg.write(weng + '\n')


exp_result('result/5cls/result_e1')
