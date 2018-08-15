import csv
import re
import numpy as np
import os
import itertools
import sys
from scipy import sparse

temp_count = 0


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
    print('There are ' + str(len(features)) + ' features (including ^ and $) in ' + training_data )
    return features


def feature_vector(filename, classes, fv_type="LR", ipa_feature=False):
    """
    :param filename: name of the input data file
    :param classes: names of features
    :param ipa_feature: Only supports Chinese data for now
    :param fv_type: Type of feature vectors, choices are {
        "L": [L_unigram], "R": [R_unigram],
        "LR": [L_unigram ; R_unigram],
        "bLR": [LR_bigram],
        "LRbLR": [L_unigram ; R_unigram ; LR_bigram]
        "LL": [L_alt_unigram ; L_unigram ]
        "RR": [R_unigram ; R_alt_unigram]
        "LLR": LL + R
        "RRL": RR + L
        "LL_RR_LR": LL + RR + LR
        }
    :return: a csv file storing the feature vectors for every character in the input data file
    """

    cl_left = [cl for cl in classes if not cl == '$']  # '$' cannot appear in the left context
    cl_right = [cl for cl in classes if not cl == '^']  # '^' cannot appear in the right context
    cl_blr = ["".join(cl) for cl in itertools.product(cl_left, cl_right)]
    cl_blr.remove("^$")  # '^$' just means empty data

    features_dict = {
        'L': cl_left,
        'R': cl_right,
        'LR': cl_left + cl_right,
        'bLR': cl_blr,
        'LRbLR': cl_left + cl_right + cl_blr,
        'LL': cl_left + cl_left,
        'RR': cl_right + cl_right,
        "LLR": cl_left + cl_left + cl_right,
        "RRL": cl_right + cl_right + cl_left,
        "LL_RR_LR": cl_left + cl_left + cl_right + cl_right + cl_left + cl_right
    }

    cl_names = features_dict[fv_type] + []  # [] prevents reference conflict

    ipa_chars = []  # initialize ipa data as an empty list
    if ipa_feature:
        print('Enable IPA features!')
        ipa = load_ipa()  # where needed to be changed if there is another IPA table
        ipa_cls = ipa['flattened_classes']
        ipa_chars = ipa['ordered_contents']
        cl_names += ipa_cls + ipa_cls

    with open(filename, 'r', encoding='UTF-8-sig') as data:
        dictionary = [word.replace('\n', '').replace(' ', '') for word in data.readlines()]
        print(str(len(dictionary)) + ' data are loaded!')
        print('The first three data are: ' + str(dictionary[0:3]))

    # Store the fvs into a sparse matrix
    spa_matrix = []
    for word in dictionary:
        feature_vectors = feature_vector_word(word, features_dict, fv_type, ipa_chars)
        fvs = feature_vectors
        assert len(fvs) == len(word)
        spa_matrix += fvs
    spa_matrix = sparse.vstack(spa_matrix)
    sparse.save_npz(filename[:len(filename)-4] + '_fvs', spa_matrix)
    print('Shape of features matrix generated: ' + str(spa_matrix.shape))
    print('Number of classes ' + str(len(cl_names)))
    assert spa_matrix.shape[1] == len(cl_names)


# uni-gram feature_vector generator for both Chinese and English
def feature_vector_word(ori_word, feaures_dict, fv_type, ipa_chars):
    # prepare data to be fed to Seq2Seq model

    cl_left = feaures_dict['L']
    cl_right = feaures_dict['R']
    cl_blr = feaures_dict['bLR']

    assert len(cl_left) == len(cl_right)
    assert len(cl_left) * len(cl_right) == len(cl_blr) + 1

    cl_left = np.asmatrix(cl_left)
    cl_right = np.asmatrix(cl_right)
    cl_blr = np.asmatrix(cl_blr)

    word = '^' + ori_word + '$'  # add the ^ and $ as start end symbol

    rows = []
    for i in range(len(word)):
        if word[i] == '^' or word[i] == '$':
            continue
        else:
            # Check left unigram
            left_unigram = word[i-1]
            left = cl_left == left_unigram
            left = [int(boolean) for boolean in left.tolist()[0]]  # change logical matrix to numerical list

            # Check right unigram
            right_unigram = word[i+1]
            right = cl_right == right_unigram
            right = [int(boolean) for boolean in right.tolist()[0]]  # change logical matrix to numerical list

            # Check left_right bigram
            lr_bigram = left_unigram + right_unigram  # e.g. word: abc, looking at b, it's ac.
            lr = cl_blr == lr_bigram
            lr = [int(boolean) for boolean in lr.tolist()[0]]  # change logical matrix to numerical list

            # Check left_two_unigrams
            if i == 1:  # Deal with the initial character (not ^)
                assert left_unigram == '^'
                left_alt_unigram = left_unigram  # add another ^ to deal with the marginal case
            else:
                left_alt_unigram = word[i-2]
            left_alt = cl_left == left_alt_unigram
            left_alt = [int(boolean) for boolean in left_alt.tolist()[0]]  # change logical matrix to numerical list

            # Check right_two_unigrams
            if i == len(word) - 2: # Deal with the last character (not $)
                assert right_unigram == '$'
                right_alt_unigram = right_unigram # add another $ to dea with the marginal case
            else:
                right_alt_unigram = word[i+2]
            right_alt = cl_right == right_alt_unigram
            right_alt = [int(boolean) for boolean in right_alt.tolist()[0]]  # change logical matrix to numerical list

            # form a single feature vector
            row_dict = {
                "L": left,
                "R": right,
                "LR": left + right,
                "bLR": lr,
                "LRbLR": left + right + lr,
                "LL": left_alt + left,
                "RR": right + right_alt,
                "LLR": left_alt + left + right,
                "RRL": right + right_alt + left,
                "LL_RR_LR":  left_alt + left + right + right_alt + left + right
            }
            row = row_dict[fv_type]

            if 1 not in left:
                print(left_unigram + ' is an unknown character in the training dataset.')
            if 1 not in right:
                print(right_unigram + ' is an unknown character in the training dataset.')

            # The IPA features used here are of the form [Left_char_IPA; Right_char_IPA]
            if not ipa_chars == []:
                num_ipa_classes = len(ipa_chars)
                left_ipa = [0] * num_ipa_classes
                right_ipa = [0] * num_ipa_classes
                for j in range(num_ipa_classes):
                    options = ipa_chars[j]
                    if left_unigram in options:  # If the left char is in the IPA cell
                        left_ipa[j] = 1
                        # print(str(i) + ' left IPA is ' + str(ipa_cls[j]))
                    if right_unigram in options:  # If the right char is in the IPA cell
                        right_ipa[j] = 1
                        # print(str(i) + ' right IPA is ' + str(ipa_cls[j]))
                row = row + left_ipa + right_ipa
            else:
                # assert sum(row) == 2
                pass

            # save the feature vector in a sparse manner (save memory)
            # also, csr_matrix supports fancy indexing, so easier smoothing
            row = sparse.csr_matrix(np.array(row))

            rows.append(row)
            print(word[i] + ' of ' + ori_word)
    assert len(rows) == len(word)-2
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


def feature_vector_all(src, src_fv_type, tgt, tgt_fv_type):
    # Since it is inductive learning, features are extracted from training data only
    src_features = get_features(src + "_tra.txt")
    tgt_features = get_features(tgt + "_tra.txt")

    for title in ['tra', 'dev', 'tst']:
        feature_vector(src + '_' + title + '.txt', src_features, src_fv_type)
        if tgt == 'ch':
            print('Target language is Chinese, enable IPA feaures.')
            feature_vector(tgt + '_' + title + '.txt', tgt_features, tgt_fv_type, ipa_feature=True)
        else:
            feature_vector(tgt + '_' + title + '.txt', tgt_features, tgt_fv_type)

        # assert


if __name__ == "__main__":

    data_dir = input("Please enter the directory where the required original data files exist\n--->  ")
    os.chdir(data_dir)

    print("The arguments format is: flag, src_language, src_features_type, tgt_language, tgt_features_type")
    feature_vector_all(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])



