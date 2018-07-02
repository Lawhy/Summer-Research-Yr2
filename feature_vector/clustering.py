import numpy as np
import csv
from sklearn.cluster import KMeans


# load the feature vectors data
def load_fv(lan):
    with open('fv_' + lan + '.csv', 'r', encoding='UTF-8-sig') as eng:
        reader = csv.reader(eng)
        fst = True
        fvs = []
        ordered_char = []
        ordered_word = []
        for fv in reader:
            if fst:
                dim = len(fv) - 3
                fst = False
                col_names = fv
            else:
                assert len(fv) - 2 == dim
                ordered_char.append(fv[len(fv)-2])
                ordered_word.append(fv[len(fv)-1])
                fvs.append(fv[:len(fv)-2])
        fvs = np.array(fvs).astype(np.int)
        print('Feature vectors data loaded in language: ' + lan)
        print('Number of data loaded: ' + str(len(fvs)))
        print('Shape of data matrix: ' + str(fvs.shape))
        # print('First two feature vectors are:')
        # print(fvs[0:2])
        return {
            'titles': col_names,
            'chars': ordered_char,
            'words': ordered_word,
            'fvs': fvs
        }


def smoothing(data, threshold=3):
    cls = data['titles']
    fvs = data['fvs']
    column_sum = np.sum(fvs, axis=0)
    # print(column_sum)
    less_than_threshold = column_sum <= threshold
    col_index_to_be_removed = []
    count = 0
    for i in range(len(less_than_threshold)):
        if less_than_threshold[i]:
            count += 1
            col_index_to_be_removed.append(i)
    # print(col_index_to_be_removed)
    print('There are ' + str(count) + ' columns less than the threshold: ' + str(threshold))
    smoothed_fvs = np.delete(fvs, col_index_to_be_removed, axis=1)  # key functioning here
    smoothed_cls = [np.array(cls).astype(np.str)]   # to make the shape as (1, n_features) instead of (,n_features)
    smoothed_cls = np.delete(smoothed_cls, col_index_to_be_removed, axis=1)
    print(smoothed_fvs.shape)
    print(smoothed_cls.shape)

    return {
        # both are of type nd_arrays
        'fvs': smoothed_fvs,
        'titles': smoothed_cls,
        # for check use
        'removed_index': col_index_to_be_removed
    }


def clustering_kmeans(lan, n_clusters):
    data = load_fv(lan)
    chars = data['chars']
    words = data['words']
    if lan == 'eng':
        fvs = data['fvs']
        # cls = data['titles']

        # load eva and tst data for prediction
        eva_data = load_fv('eng_eva')
        eva_fvs = eva_data['fvs']
        eva_chars = eva_data['chars']
        eva_words = eva_data['words']

        tst_data = load_fv('eng_tst')
        tst_fvs = tst_data['fvs']
        tst_chars = tst_data['chars']
        tst_words = tst_data['words']
    elif lan == 'chi':
        smooth = smoothing(data)
        fvs = smooth['fvs']
        col_index_to_be_removed = smooth['removed_index']
        # cls = smooth['titles']
        # cls = cls[0].tolist()

        # load eva and tst data for prediction
        eva_data = load_fv('chi_dev')
        eva_fvs = eva_data['fvs']
        eva_fvs = np.delete(eva_fvs, col_index_to_be_removed, axis=1)  # smooth evaluation matrix
        eva_chars = eva_data['chars']
        eva_words = eva_data['words']

        tst_data = load_fv('chi_tst')
        tst_fvs = tst_data['fvs']
        tst_fvs = np.delete(tst_fvs, col_index_to_be_removed, axis=1)  # smooth evaluation matrix
        tst_chars = tst_data['chars']
        tst_words = tst_data['words']

        print('The shapes for tra, eva, tst matrices are:')
        print(fvs.shape)
        print(eva_fvs.shape)
        print(tst_fvs.shape)
    else:
        print("Invalid language!")
    # using k-means algorithm to learn clustering of training dataset and predict the evaluation and test dataset
    k_means = KMeans(n_clusters=n_clusters, init='k-means++')
    k_means = k_means.fit(fvs)
    clusters = k_means.labels_
    eva_clus = k_means.predict(eva_fvs)
    tst_clus = k_means.predict(tst_fvs)
    assert len(chars) == len(words)
    assert len(words) == len(clusters)
    # form labelled training dataset
    with open('en2chi_tra_' + lan + '_' + str(n_clusters) + 'cls.txt', 'w+', encoding='UTF-8') as output:
        cur_labelled_word = []
        for i in range(len(chars)):
            cur_char = chars[i]
            cur_label = clusters[i]
            cur_labelled_word.append(cur_char + '-' + str(cur_label))
            if i+1 == len(chars):
                print('last training word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                output.write(cur_labelled_word + '\n')
                break
            # skip to the next word and store the current word
            if words[i+1] != words[i]:
                # print('next word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                output.write(cur_labelled_word + '\n')
                cur_labelled_word = []
    # form labelled evaluation dataset
    with open('en2chi_dev_' + lan + '_' + str(n_clusters) + 'cls.txt', 'w+', encoding='UTF-8') as op_eva:
        cur_labelled_word = []
        for i in range(len(eva_chars)):
            cur_char = eva_chars[i]
            cur_label = eva_clus[i]
            cur_labelled_word.append(cur_char + '-' + str(cur_label))
            if i+1 == len(eva_chars):
                print('last evaluation word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                op_eva.write(cur_labelled_word + '\n')
                break
            # skip to the next word and store the current word
            if eva_words[i+1] != eva_words[i]:
                # print('next word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                op_eva.write(cur_labelled_word + '\n')
                cur_labelled_word = []
    # form labelled test dataset
    with open('en2chi_tst_' + lan + '_' + str(n_clusters) + 'cls.txt', 'w+', encoding='UTF-8') as op_tst:
        cur_labelled_word = []
        for i in range(len(tst_chars)):
            cur_char = tst_chars[i]
            cur_label = tst_clus[i]
            cur_labelled_word.append(cur_char + '-' + str(cur_label))
            if i+1 == len(tst_chars):
                print('last testing word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                op_tst.write(cur_labelled_word + '\n')
                break
            # skip to the next word and store the current word
            if tst_words[i+1] != tst_words[i]:
                # print('next word!')
                cur_labelled_word = ' '.join(cur_labelled_word)
                op_tst.write(cur_labelled_word + '\n')
                cur_labelled_word = []

    # with open('fv_' + lan + '_labelled_sample.csv', 'w+', encoding='UTF-8', newline='') as fl:
    #     wr = csv.writer(fl)
    #     wr.writerow(cls)
    #     ind = 0
    #     fvs = fvs.tolist()
    #     while ind < 30:
    #         wr.writerow(fvs[ind] + [chars[ind]] + [words[ind]] + [clusters[ind]])
    #         print([chars[ind]] + [words[ind]] + [clusters[ind]])
    #         ind += 1


if __name__ == '__main__':
    clustering_kmeans('chi', 15)


