import re


def count_wer(pred, ans):
    chi = r'[\u4E00-\u9FA5]'
    pa = re.compile(chi)

    with open(pred, 'r', encoding='UTF-8') as f:
        preds = f.readlines()

    with open(ans, 'r', encoding='UTF-8') as tst:
            answers = tst.readlines()

    assert len(preds) == len(answers)

    count_WER = 0
    predictions = []

    for i in range(len(preds)):

        predict = re.findall(pa, preds[i])
        answer = re.findall(pa, answers[i])
        predict = ' '.join(predict)
        answer = ' '.join(answer)
        predictions.append(predict)
        # count WER
        if predict == answer:
            count_WER += 1

        print(predict + ' | ' + answer)

    with open('./dev/' + pred[0: len(pred)-4] + '_ori.txt', 'w+', encoding='UTF-8') as pr:
        for pre in predictions:
            pr.write(pre + '\n')

    w_acc = count_WER/len(answers)
    print('WER: ' + str(1 - w_acc))
    print(len(answers))
    return 1 - w_acc


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

count_wer('pred.txt', './baseline/en2chi_dev_chi.txt')

