import csv

consonants = {
    # left: simplified representation
    '-': ['Null'],
    'b': ['b'],
    'p': ['p'],
    'd': ['d'],
    't': ['t'],
    'g': ['g'],
    'k': ['k'],
    'v': ['v'],
    'w': ['w'],
    'f': ['f'],
    'z': ['z', 'dz'],
    'ts': ['ts'],
    's': ['s', 'ð', 'θ'],
    'ge': ['ʒ'],
    'sh': ['ʃ'],
    'gi': ['dʒ'],
    'chi': ['tʃ'],
    'h': ['h'],
    'm': ['m'],
    'n': ['n'],
    'l': ['l'],
    'r': ['ɹ'],
    'j': ['j'],
    'gw': ['ɡʷ'],
    'kw': ['kʷ'],
    'hw': ['hʷ'],
    'tr': ['tr'],  # e.g. Tracy
    'di': ['di']   # e.g. Diego
}

vowels = {
    '-': ['Null'],
    'a': ['ɑː', 'æ', 'ʌ'],
    'ei': ['e', 'eɪ'],
    'er': ['ɜ', 'ə'],
    'i': ['iː', 'ɪ'],
    'o': ['ɒ', 'ɔː', 'oʊ', 'o', 'əʊ'],
    'u': ['uː', 'ʊ'],
    'jo': ['juː', 'jʊ'],
    'ai': ['aɪ'],
    'ao': ['aʊ'],
    'an': ['æn', 'ʌn', 'an', 'æŋ'],
    'ang': ['ɑn', 'aʊn', 'ʌŋ', 'ɔːn', 'ɒn', 'ɒŋ'],
    'en': ['ɛn', 'ɛŋ', 'ɜːn', 'ən', 'əŋ'],
    'in': ['ɪn', 'iːn', 'ɪən', 'jən'],
    'ing': ['ɪŋ'],
    'un': ['uːn', 'ʊn', 'oʊn'],
    'ung': ['ʊŋ']
}

# with open('TABLE.txt', 'r', encoding='UTF-8') as tb:
#     lines = tb.readlines()
#
# for line in lines:
#     tst = line.split('\t')
#     assert len(tst) == 29
# with open('Table_prototype' + '.csv', 'w+', encoding='UTF-8', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow([''] + list(consonants.values()))
#     vos = list(vowels.values())
#     fst = True
#     index = 0
#     for line in lines:
#         if fst:
#             fst = False
#             continue
#         lst = line.split('\t')
#         lst[0] = vos[index]
#         csv_writer.writerow(lst)
#         index += 1
#         fst = False
