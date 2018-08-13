import yaml


def data_yaml(cls_num):
    data_instruct = dict(
    model_dir = 'en2chi_models',
    data = dict(
        train_features_file = '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters/en2chi_tra_eng_' + cls_num + 'cls.txt',
        train_labels_file = '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters/en2chi_tra_chi_' + cls_num + 'cls.txt',
        eval_features_file = '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters/en2chi_dev_eng_'+ cls_num + 'cls.txt',
        eval_labels_file =  '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters/en2chi_dev_chi_' + cls_num + 'cls.txt',
        source_words_vocabulary = '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters_vocab/en2chi_tra_eng_' + cls_num + 'cls_vocab.txt',
        target_words_vocabulary = '/disk/ocean/lhe/OpenNMT-tf/' + cls_num + '_clusters_vocab/en2chi_tra_chi_' + cls_num + 'cls_vocab.txt'
        )
    )

    with open('en2chi_' + cls_num + 'cls.yml', 'w') as output:
        yaml.dump(data_instruct, output, default_flow_style=False)

