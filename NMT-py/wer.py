import re
import sys


def count_wer(pred, ans):
    char = r'(\w?)￨[0-9]'   # take the cluster numbers away
    pa = re.compile(char)

    with open(pred, 'r', encoding='UTF-8-sig') as f:
        preds = f.readlines()

    with open(ans, 'r', encoding='UTF-8-sig') as tst:
        answers = tst.readlines()

    assert len(preds) == len(answers)

    correct = 0
    predictions = []

    for i in range(len(preds)):

        predict = re.findall(pa, preds[i])

        if not predict:
            predict = preds[i].replace('\n', '')
        else:
            predict = ' '.join(predict)

        answer = answers[i].replace('\n', '')
        predictions.append(predict)
        # count WER
        if predict == answer:
            correct += 1

        # print(predict + ' | ' + answer)

    with open(pred[0: len(pred)-4] + '_ori.txt', 'w+', encoding='UTF-8-sig') as pr:
        for pre in predictions:
            pr.write(pre + '\n')

    w_acc = correct/len(answers)
    print('WER: ' + str(1 - w_acc))
    print(len(answers))
    return 1 - w_acc


if __name__ == '__main__':
    count_wer(sys.argv[1], sys.argv[2])
