import csv
import re
import numpy as np
import time
import os

# loading the names of classes for data alignment check (better visualisation)
eng_cls = ['^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\'', '$']


# obtain features from well-formatted training data file
def get_features(training_data):
    # each line should contain a word and each character is separated by a space
    with open(training_data, 'r', encoding='UTF-8-sig') as tra:
        words = [line.replace(' ', '').replace('\n', '') for line in tra.readlines()]
    features = set()
    for word in words:
        for char in word:
            features.add(char)
    features = list(features)
    features = ['^', '$'] + features
    print('There are ' + str(len(features)) + ' features in ' + training_data )
    return features


def feature_vector_all(filename, classes, ipa_feature=False):

        cl_left = [cl for cl in classes if not cl == '$']  # '$' cannot appear in the left context
        cl_right = [cl for cl in classes if not cl == '^']  # '^' cannot appear in the right context
        ipa_chars = []  # initialize ipa data as an empty list

        if ipa_feature:
            print('Enable IPA features!')
            ipa = load_ipa()  # where needed to be changed if there is another IPA table
            ipa_cls = ipa['flattened_classes']
            ipa_chars = ipa['ordered_contents']

        with open(filename, 'r', encoding='UTF-8-sig') as data:
            dictionary = [word.replace('\n', '').replace(' ', '') for word in data.readlines()]
            print(str(len(dictionary)) + ' data are loaded!')
            print('The first three data are: ' + str(dictionary[0:3]))

        with open(filename[:len(filename)-4] + '_fvs.csv', 'w+', encoding='UTF-8', newline='') as output:
            total = 0
            writer = csv.writer(output)
            cl_names = cl_left + cl_right
            if ipa_feature:
                cl_names += ipa_cls
                cl_names += ipa_cls
            cl_names.append('Char')
            cl_names.append('Word')
            writer.writerow(cl_names)
            for word in dictionary:
                count = 0
                feature_vectors = feature_vector_unigram(word, cl_left, cl_right, ipa_chars)
                # print(feature_vectors)
                for vec in feature_vectors:
                    writer.writerow(vec)
                    total += 1
                    count += 1
                # print('There are ' + str(count) + ' characters in the word: ' + word)
            print('Number of feature vectors generated: ' + str(total))


# uni-gram feature_vector generator for both Chinese and English
def feature_vector_unigram(ori_word, cl_left, cl_right, ipa_chars):
    # prepare data to be fed to Seq2Seq model
    assert len(cl_left) == len(cl_right)
    # cls = cl_left + cl_right + ['Char'] + ['Word'] + ['Class']

    cl_left = np.asmatrix(cl_left)
    cl_right = np.asmatrix(cl_right)

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
            if 1 not in left:
                print(left_unigram + ' is an unknown character in the training dataset.')
            if 1 not in right:
                print(right_unigram + ' is an unknown character in the training dataset.')

            if not ipa_chars == []:
                num_ipa_classes = len(ipa_chars)
                left_ipa = [0] * num_ipa_classes
                right_ipa = [0] * num_ipa_classes
                for j in range(num_ipa_classes):
                    options = ipa_chars[j]
                    if left_unigram in options:
                        left_ipa[j] = 1
                        # print(str(i) + ' left IPA is ' + str(ipa_cls[j]))
                    if right_unigram in options:
                        right_ipa[j] = 1
                        # print(str(i) + ' right IPA is ' + str(ipa_cls[j]))
                row = row + left_ipa + right_ipa
                # if not len(ori_word) == 1:
                #     assert sum(row) >= 3

            row.append(word[i])
            row.append(ori_word)
            rows.append(row)
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

    with open('IPA_table_flatten.csv', 'w+', encoding='UTF-8', newline='') as ft:
        writer = csv.writer(ft)
        writer.writerow(flattened_classes)
        writer.writerow(ordered_contents)
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


if __name__ == "__main__":
    # The features are determined only by the training data (inductive learning)

    # os.chdir('./data/ar/bs')
    # ar = get_features('ar_tra.txt')
    # en = get_features('en_tra.txt')
    # feature_vector_all('ar_tra.txt', ar)
    # feature_vector_all('ar_dev.txt', ar)
    # feature_vector_all('ar_tst.txt', ar)
    # feature_vector_all('en_tra.txt', en)
    # feature_vector_all('en_dev.txt', en)
    # feature_vector_all('en_tst.txt', en)

    # os.chdir('./data/jp/bs')
    # jp = get_features('jp_tra.txt')
    # en = get_features('en_tra.txt')
    # feature_vector_all('jp_tra.txt', jp)
    # feature_vector_all('jp_dev.txt', jp)
    # feature_vector_all('jp_tst.txt', jp)
    # feature_vector_all('en_tra.txt', en)
    # feature_vector_all('en_dev.txt', en)
    # feature_vector_all('en_tst.txt', en)

    os.chdir('./data/he/bs')
    he = get_features('he_tra.txt')
    en = get_features('en_tra.txt')
    feature_vector_all('he_tra.txt', he)
    feature_vector_all('he_dev.txt', he)
    feature_vector_all('he_tst.txt', he)
    feature_vector_all('en_tra.txt', en)
    feature_vector_all('en_dev.txt', en)
    feature_vector_all('en_tst.txt', en)

    # # Check Chinese IPA
    # with open('CHI/bs/chi_tst_fvs.csv', 'r', encoding='UTF-8') as tst:
    #     reader = csv.reader(tst)
    #     num = 0
    #     for line in reader:
    #         if num == 0:
    #             features = line
    #         if num >= 5:
    #             break
    #         if num > 0:
    #             content = line[:len(line)-2]
    #             inds = []
    #             for i in range(len(content)):
    #                 n = int(content[i])
    #                 if n == 1:
    #                     inds.append(i)
    #             for j in inds:
    #                 print(features[j] + ' is a fv component of ' + line[len(line)-2])
    #
    #         num += 1


