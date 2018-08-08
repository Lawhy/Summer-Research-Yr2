import re
import sys


def bst_ckp(wer, cer):
    with open(wer, 'r', encoding='UTF-8') as w:
        wers = w.readlines()
    with open(cer, 'r', encoding='UTF-8') as c:
        cers = c.readlines()

    t_steps = []
    wrs = []
    crs = []
    pa_wer = re.compile(r'WER: (.+)')
    pa_cer = re.compile(r'CER:    (.+)%')

    for i in range(0, len(wers), 2):
        wer = re.findall(pa_wer, wers[i])
        assert wer != []
        t_steps.append(wers[i+1].replace('\n', ''))
        wer = round(float(wer[0]), 5)
        wrs.append(wer)

    for i in range(0, len(cers), 2):
        cer = re.findall(pa_cer, cers[i])
        assert cer != []
        cer = round(float(cer[0])/100, 5)
        crs.append(cer)

    assert len(t_steps) == 10

    min_wer = min(wrs)
    cer_for_min_wer = 1
    bst_ckp = 0

    # If two wers are equal, choose the one with lower cer
    for i in range(len(wrs)):
        if wrs[i] == min_wer and crs[i] < cer_for_min_wer:
            cer_for_min_wer = crs[i]
            bst_ckp = t_steps[i]

    print('Best checkpoint: ' + str(bst_ckp))
    print('WER: ' + str(min_wer))
    print('CER: ' + str(cer_for_min_wer))


if __name__ ==  '__main__':
    bst_ckp(sys.argv[1], sys.argv[2])
