import itertools
import csv
import re
import numpy as np
import time

eng_col = ['^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\'', '$']


# uni-gram feature_vector generator for both Chinese and English
def feature_vector_unigram(ori_word, cl_left, cl_right, ipa=[]):
    # prepare data to be fed to Seq2Seq model
    assert len(cl_left) == len(cl_right)
    # cls = cl_left + cl_right + ['Char'] + ['Word'] + ['Class']

    cl_left = np.asmatrix(cl_left)
    cl_right = np.asmatrix(cl_right)

    if not ipa == []:
        ipa_data = load_ipa()
        print('Enable IPA features!')
        ipa_cls = ipa_data['flattened_classes']
        ipa_chars = ipa_data['ordered_contents']

    word = '^' + ori_word.lower() + '$'  # add the ^^ and $$ for simpler calculation
    rows = []
    for i in range(len(word)):
        if word[i] == '^' or word[i] == '$':
            continue
        else:
            left_unigram = word[i-1]
            left = cl_left == left_unigram
            left = [int(boolean) for boolean in left.tolist()[0]]

            right_unigram = word[i+1]
            right = cl_right == right_unigram
            right = [int(boolean) for boolean in right.tolist()[0]]

            row = left + right

            if not ipa == []:
                num_ipa_classes = len(ipa_chars)
                left_ipa = [0] * num_ipa_classes
                right_ipa = [0] * num_ipa_classes
                for j in range(num_ipa_classes):
                    options = ipa_chars[j]
                    if left_unigram in options:
                        left_ipa[j] = 1
                        print(str(i) + ' left IPA is ' + str(ipa_cls[j]))
                    if right_unigram in options:
                        right_ipa[j] = 1
                        print(str(i) + ' right IPA is ' + str(ipa_cls[j]))
                row = row + left_ipa + right_ipa

            row.append(word[i])
            row.append(ori_word)
            rows.append(row)
    # with open('test.csv', 'w+', encoding='UTF-8', newline='') as t:
    #     wr = csv.writer(t)
    #     cl_names = cl_left.tolist()[0] + cl_right.tolist()[0]
    #     if not ipa == []:
    #         cl_names += ipa_cls
    #         cl_names += ipa_cls
    #     cl_names.append('Char')
    #     cl_names.append('Word')
    #     cl_names.append('Class')
    #     wr.writerow(cl_names)
    #     for row in rows:
    #         wr.writerow(row)

    return rows


# Transform the 2-D table into 1-D flatted version
def flatten_table(table_name):
    with open(table_name + '.csv', 'r', encoding='UTF-8') as ipa:
        reader = csv.reader(ipa)
        fst = True
        flattened_classes = []
        ordered_contents = []
        for row in reader:
            if fst:
                fst = False
                consonants = row
                continue
            for i in range(len(row)):
                if i == 0:
                    cur_vow = row[0]
                else:
                    cur_class = consonants[i] + cur_vow
                    # consider only those non-empty cells (so as to reduce the dimensions of feature vectors)
                    if bool(re.match(r'[\u4E00-\u9FA5]', row[i])):
                        flattened_classes.append(cur_class)
                        ordered_contents.append(row[i])

    # with open('flatten_table.csv', 'w+', encoding='UTF-8', newline='') as ft:
    #     writer = csv.writer(ft)
    #     writer.writerow(flatten_classes)
    #     writer.writerow(ordered_contents)
    assert len(flattened_classes) == len(ordered_contents)
    return {
        'flattened_classes': flattened_classes,
        'ordered_contents': ordered_contents
    }


def load_ipa():
    with open('IPA_table_flatten.csv', 'r', encoding='UTF-8') as ft:
        reader = csv.reader(ft)
        fst = True
        for row in reader:
            if fst:
                flattened_classes = row
                fst = False
            else:
                ordered_contents = row
        return {
            'flattened_classes': flattened_classes,
            'ordered_contents': ordered_contents
        }


# feature_vector_unigram('Amy', eng_col)
