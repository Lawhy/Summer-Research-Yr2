def count_vocab(filename):
    vocab = set()
    with open(filename, 'r', encoding='UTF-8-sig') as f:
        words = f.readlines()
    for word in words:
        word = word.replace('\n', '')
        chars = word.split(' ')
        # print(chars)
        for char in chars:
            vocab.add(char)
    print("The size of vocab is: " + str(len(vocab)))
    return vocab


def count_diff(path_tra, path_dev_or_tst):
    tra = count_vocab(path_tra)
    dev_or_tst = count_vocab(path_dev_or_tst)
    diff = 0
    for voc in dev_or_tst:
        if voc not in tra:
            print(voc)
            diff += 1


def merge_files(tra, dev, tst, lan, cls=''):
    with open(tra, 'r', encoding='UTF-8-sig') as f:
        data_tr = f.readlines()
    with open(dev, 'r', encoding='UTF-8-sig') as f:
        data_dev = f.readlines()
    with open(tst, 'r', encoding='UTF-8-sig') as f:
        data_tst = f.readlines()
    data = data_tr + data_dev + data_tst
    with open(lan + cls + '.txt', 'w+', encoding='UTF-8') as output:
        output.writelines(data)


# merge_files('en2chi_tra_eng_10cls.txt', 'en2chi_dev_eng_10cls.txt', 'en2chi_tst_eng_10cls.txt', 'eng', '_10cls')
count_diff('en2chi_tra_eng_10cls.txt', 'en2chi_tst_eng_10cls.txt')