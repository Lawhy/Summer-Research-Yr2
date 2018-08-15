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

chi = count_vocab('ru_tra.txt')
print(len(chi))
chi_dev = count_vocab('ru_tst.txt')
diff = 0
for voc in chi_dev:
    if voc not in chi:
        print(voc)
        diff += 1
print(diff)