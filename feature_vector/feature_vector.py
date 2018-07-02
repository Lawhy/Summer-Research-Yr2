import csv
import re
import numpy as np
import time

# loading the names of classes for data alignment check (better visualisation)
eng_cls = ['^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\'', '$']
with open('./data/chi_char.txt', 'r', encoding='UTF-8-sig') as cc:
    chi_cls = [chi.replace('\n', '') for chi in cc.readlines()]
    han = r'^[\u4E00-\u9FA5]$'
    for chi in chi_cls:
        assert bool(re.match(han, chi))
    chi_cls = ['^'] + chi_cls + ['$']


def feature_vector_all(filename, classes, ipa_feature=False):

        cl_left = [cl for cl in classes if not cl == '$']  # '$' cannot appear in the left context
        cl_right = [cl for cl in classes if not cl == '^']  # '^' cannot appear in the right context
        ipa_chars = []  # initialize ipa data as an empty list

        if ipa_feature:
            print('Enable IPA features!')
            ipa = load_ipa()
            ipa_cls = ipa['flattened_classes']
            ipa_chars = ipa['ordered_contents']

        with open(filename, 'r', encoding='UTF-8-sig') as data:
            dictionary = [word.replace('\n', '') for word in data.readlines()]
            print(str(len(dictionary)) + ' data are loaded!')
            print('The first three data are: ' + str(dictionary[0:3]))

        with open('feature_vectors.csv', 'w+', encoding='UTF-8', newline='') as output:
            total = 0
            writer = csv.writer(output)
            cl_names = cl_left + cl_right
            if ipa_feature:
                cl_names += ipa_cls
                cl_names += ipa_cls
            cl_names.append('Char')
            cl_names.append('Word')
            cl_names.append('Cluster')
            writer.writerow(cl_names)
            for word in dictionary:
                count = 0
                feature_vectors = feature_vector_unigram(word, cl_left, cl_right, ipa_chars)
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
    # with open('test.csv', 'w+', encoding='UTF-8', newline='') as t:
    #     wr = csv.writer(t)
    #     cl_names = cl_left.tolist()[0] + cl_right.tolist()[0]
    #     if not ipa == []:
    #         cl_names += ipa_cls
    #         cl_names += ipa_cls
    #     cl_names.append('Char')
    #     cl_names.append('Word')
    #     cl_names.append('Cluster')
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


def chi_char(s):
    chi_set = set()
    chi = r'[\u4E00-\u9FA5]'
    with open(s + '.txt', 'r', encoding='UTF-8-sig') as f:
        lines = f.readlines()
        print(lines)
    for line in lines:
        for char in line:
            if bool(re.match(chi, char)):
                chi_set.add(char)
    with open('chi_char.txt', 'w+', encoding='UTF-8') as output:
        for char in chi_set:
            output.write(char + '\n')
    return chi_set


if __name__ == "__main__":
    flatten_table('IPA_Table_1.0')  # this line should only be executed if there is some change made in the IPA_Table
    # The following code can generate the feature vectors
    # Run each line separately, and change the name of output file to 'fv_*' format for clustering purpose.
    # feature_vector_all('./data/en2chi_tra_chi.txt', chi_cls, ipa_feature=True)
    # feature_vector_all('./data/en2chi_dev_chi.txt', chi_cls, ipa_feature=True)
    # feature_vector_all('./data/en2chi_tst_chi.txt', chi_cls, ipa_feature=True)
    # feature_vector_all('./data/en2chi_tra_eng.txt', eng_cls, ipa_feature=False)
    # feature_vector_all('./data/en2chi_dev_eng.txt', eng_cls, ipa_feature=False)
    # feature_vector_all('./data/en2chi_tst_eng.txt', eng_cls, ipa_feature=False)
