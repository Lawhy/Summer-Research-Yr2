import numpy as np
import csv
from sklearn.cluster import KMeans


# load the feature vectors data
def load_fv(lan, tra_or_dev_or_tst):
    with open(lan + '_' + tra_or_dev_or_tst + '_' + 'fvs.csv', 'r', encoding='UTF-8-sig') as eng:
        reader = csv.reader(eng)
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
    print('The shape after summing: ' + str(column_sum.shape))
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


def clustering_kmeans(lan, n_clusters, smooth=False):

    # loading tra dev tst data
    tra = load_fv(lan, 'tra')
    tra_fvs = tra['fvs']
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
        smooth = smoothing(tra)
        tra_fvs = smooth['fvs']
        col_index_to_be_removed = smooth['removed_index']
        dev_fvs = np.delete(dev_fvs, col_index_to_be_removed, axis=1)  # smooth dev matrix
        tst_fvs = np.delete(tst_fvs, col_index_to_be_removed, axis=1)  # smooth test matrix

        print('The shapes for tra, eva, tst matrices are:')
        print(tra_fvs.shape)
        print(dev_fvs.shape)
        print(tst_fvs.shape)

    # using k-means algorithm to learn clustering of training dataset and predict the dev and test dataset
    k_means = KMeans(n_clusters=n_clusters, init='k-means++')
    k_means = k_means.fit(tra_fvs)
    tra_clus = k_means.labels_
    dev_clus = k_means.predict(dev_fvs)
    tst_clus = k_means.predict(tst_fvs)

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
        with open(lan + '_' + title + '_' + str(n_clusters) + 'cls.txt', 'w+', encoding='UTF-8') as output:
            cur_labelled_word = []
            for i in range(len(chars)):
                cur_char = chars[i]
                cur_label = clusters[i]
                cur_labelled_word.append(cur_char + '￨' + str(cur_label))
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


if __name__ == '__main__':
    print('Clustering on progress')
    # en2he
    clustering_kmeans('he', 2)
    clustering_kmeans('he', 5)
    clustering_kmeans('he', 10)
    clustering_kmeans('he', 15)
    clustering_kmeans('en', 2)
    clustering_kmeans('en', 5)
    clustering_kmeans('en', 10)
    clustering_kmeans('en', 15)


