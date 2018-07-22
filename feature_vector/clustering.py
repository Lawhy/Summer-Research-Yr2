import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import re
import os
import sys

# load the feature vectors data
def load_fv(lan, tra_or_dev_or_tst):
    with open(lan + '_' + tra_or_dev_or_tst + '_' + 'fvs.csv', 'r', encoding='UTF-8-sig') as inp:
        reader = csv.reader(inp)
        fst = True
        fvs = []
        ordered_char = []
        ordered_word = []
        for fv in reader:
            if fst:
                dim = len(fv) - 2  # the last two columns are char and word
                fst = False
                col_names = fv  # extract the features names
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
    print('The shape after summing up: ' + str(column_sum.shape))
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


def clustering(lan, n_clusters, smooth=False, threshold=3, delimiter=u'￨', algorithm="k-means"):

    """
    Required files: Tra, dev, test feature vectors csv files and original formatted data text files
    The first three can be generated using feature_vector.py
    E.g. ch_tra_fvs, ch_dev_fvs, ch_tst_fvs ; ch_tra.txt ch_dev.txt ch_tst.txt

    :param lan: Language choices: {ar, ch, he, jp, en}
    :param n_clusters: Number of clusters
    :param smooth: Boolean for enabling smoothing process
    :param threshold: default threshold=3, remove features with frequency <= threshold if smooth=True
    :param delimiter: For source data, use u'￨'; for target data, use '-'
    :param algorithm: Clustering algorithm choices: {k-means, spectral}
    :return: Three labelled data files (training, development, test)

    This method is based on inductive learning, so it learns clustering from the training data,
    and then predicts the labelling of the corresponding development and test data.

    """

    # loading tra dev tst data
    tra = load_fv(lan, 'tra')
    tra_fvs = tra['fvs']       # get the feature vectors matrix
    tra_chars = tra['chars']   # get the ordered chars
    tra_words = tra['words']   # get the ordered words

    dev = load_fv(lan, 'dev')
    dev_fvs = dev['fvs']
    dev_chars = dev['chars']
    dev_words = dev['words']

    tst = load_fv(lan, 'tst')
    tst_fvs = tst['fvs']
    tst_chars = tst['chars']
    tst_words = tst['words']

    if smooth:
        smooth = smoothing(tra, threshold=threshold)
        tra_fvs = smooth['fvs']
        col_index_to_be_removed = smooth['removed_index']
        dev_fvs = np.delete(dev_fvs, col_index_to_be_removed, axis=1)  # smooth dev matrix
        tst_fvs = np.delete(tst_fvs, col_index_to_be_removed, axis=1)  # smooth test matrix

        print('The shapes for tra, eva, tst matrices after smoothing are:')
        print(tra_fvs.shape)
        print(dev_fvs.shape)
        print(tst_fvs.shape)

    # using k-means algorithm to learn clustering of training dataset and predict the dev and test dataset
    if algorithm == 'k-means':
        k_means = KMeans(n_clusters=n_clusters, init='k-means++')
        k_means = k_means.fit(tra_fvs)
        tra_clus = k_means.labels_
        dev_clus = k_means.predict(dev_fvs)
        tst_clus = k_means.predict(tst_fvs)
    elif algorithm == 'spectral':
        spectral = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
        spectral = spectral.fit(tra_fvs)
        tra_clus = spectral.labels_
        dev_clus = spectral.fit_predict(dev_fvs)
        tst_clus = spectral.fit_predict(tst_fvs)
    else:
        print("Not a valid algorithm choice!")
        exit(1)

    # form labelled dataset
    chars_dict = {'tra': tra_chars, 'dev': dev_chars, 'tst': tst_chars}
    words_dict = {'tra': tra_words, 'dev': dev_words, 'tst': tst_words}
    clus_dict = {'tra': tra_clus, 'dev': dev_clus, 'tst': tst_clus}
    for title in ['tra', 'dev', 'tst']:
        chars = chars_dict[title]
        words = words_dict[title]
        clusters = clus_dict[title]
        assert len(chars) == len(words)
        assert len(words) == len(clusters)
        # print(len(set(words)))

        # load the original data for word alignment (prevent consecutive duplicates)
        with open(lan + '_' + title + '.txt', 'r', encoding='UTF-8-sig') as data:
            dictionary = [word.replace('\n', '').replace(' ', '') for word in data.readlines()]

        with open(lan + '_' + title + '_' + str(n_clusters) + 'cls.txt', 'w+', encoding='UTF-8') as output:
            cur_labelled_word = []

            aligned_index = 0
            aligned_word = dictionary[aligned_index]
            aligned_count = 0

            for i in range(len(chars)):
                aligned_count += 1
                cur_char = chars[i]
                cur_label = clusters[i]
                cur_labelled_word.append(cur_char + delimiter + str(cur_label))
                # deal with the marginal case
                if i+1 == len(chars):
                    print('last ' + title + ' word!')
                    cur_labelled_word = ' '.join(cur_labelled_word)
                    output.write(cur_labelled_word + '\n')
                    break
                # skip to the next word and store the current word
                # if words[i+1] != words[i]: # This line will fail for consecutive duplicates!!!
                    # print('next word!')
                if aligned_count == len(aligned_word):
                    cur_labelled_word = ' '.join(cur_labelled_word)
                    output.write(cur_labelled_word + '\n')

                    # refresh the container for next word
                    cur_labelled_word = []
                    aligned_count = 0
                    aligned_index += 1
                    aligned_word = dictionary[aligned_index]

        # Test output alignment with the original data
        with open(lan + '_' + title + '_' + str(n_clusters) + 'cls.txt', 'r', encoding='UTF-8') as test:
            t_data = test.readlines()
        char = r'(.?)' + delimiter + '[0-9]'  # take the cluster numbers away
        pa = re.compile(char)
        clean_words = [''.join(re.findall(pa, line)) for line in t_data]
        assert len(clean_words) == len(dictionary)
        for j in range(len(clean_words)):
            assert clean_words[j] == dictionary[j]

    print(str(n_clusters) + 'cls labelling finished!')


def clustering_all(lan, src_or_tgt, algorithm, clusters=[2, 5, 10, 15]):
    if src_or_tgt == 'src':
        delimiter = u'￨'
        for cls in clusters:
            clustering(lan, cls, delimiter=delimiter, algorithm=algorithm)
    elif src_or_tgt == 'tgt':
        delimiter = '-'
        for cls in clusters:
            clustering(lan, cls, delimiter=delimiter, algorithm=algorithm)
    else:
        print("Use your own delimiter? " + src_or_tgt)
        for cls in clusters:
            clustering(lan, cls, delimiter=src_or_tgt, algorithm=algorithm)


if __name__ == '__main__':

    fvs_dir = input("Please enter the directory where the required fvs files and original data files exist\n--->  ")
    os.chdir(fvs_dir)

    if len(sys.argv) == 1:  # Use within the idk
        clustering_all('en', 'tgt', 'spectral')
    elif len(sys.argv) == 4:  # Use in command lines
        algorithm = sys.argv[3]
        print(algorithm + " clustering is applied.")
        print("Default clusters: " + "[2, 5, 10, 15]")
        clustering_all(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 5:  # Use in command lines
        algorithm = sys.argv[3]
        print(algorithm + " clustering is applied.")
        clusters = []
        for i in range(4, len(sys.argv)):
            clusters.append(int(sys.argv[i]))
        print("Customized clusters: " + str(clusters))
        clustering_all(sys.argv[1], sys.argv[2], sys.argv[3], clusters)


