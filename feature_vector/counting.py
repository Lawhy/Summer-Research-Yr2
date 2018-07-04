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

count_vocab('./labelled_data/5_clusters/en2chi_tra_chi_5cls.txt')