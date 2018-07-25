import os

main_dir = "C:\\Users\\msi-cn\\Desktop\\Transliteration\\NMT-py\\analyse"

with open("ch_dev.txt", 'r', encoding='UTF-8-sig') as ans:
    refs = ans.readlines()

with open("en_dev.txt", 'r', encoding='UTF-8-sig') as eng:
    oris = eng.readlines()


def diff(sub, cls="bs"):
    os.chdir(main_dir + "/ch/" + sub)

    for name in os.listdir(os.curdir):
        if "original" in name and cls == "bs":
            pred = name
            print("Bs data")
        elif "original" in name and (name[9] == cls or name[9:11] == cls):
            pred = name
            print(sub + " " + cls + "cls data")

    with open(pred, 'r', encoding='UTF-8-sig') as p:
        hyps = p.readlines()

    assert len(refs) == len(hyps)
    assert len(hyps) == len(oris)

    wrong = []
    for i in range(len(refs)):
        if hyps[i].replace("\n", "") != refs[i].replace("\n", ""):
            wrong.append(hyps[i].replace("\n", "").replace(" ", "") + " | " +
                         refs[i].replace("\n", "").replace(" ", "") + " | " +
                         oris[i].replace(" ", ""))

    with open("anal/" + cls + "_anal.txt", 'w+', encoding='UTF-8-sig') as output:
        output.writelines(wrong)

    print("WER: " + str(len(wrong)/len(refs)))


#for cls in ["2", "5", "10", "15"]:
    # diff("m+-", cls)
    # diff("m++", cls)
    # diff("m-+", cls)

def compare(better, worse):
    with open(better, 'r', encoding='UTF-8-sig') as bt:
        bts = bt.readlines()
    with open(worse, 'r', encoding='UTF-8-sig') as ws:
        wss = ws.readlines()

    anal = []
    for i in range(len(refs)):
        b = bts[i].replace("\n", "").replace(" ", "")
        w = wss[i].replace("\n", "").replace(" ", "")
        ref = refs[i].replace("\n", "").replace(" ", "")
        if b == ref and w != ref:
            anal.append(w + " | " + ref + " | " + oris[i].replace(" ", ""))

    with open("anal.txt", 'w+', encoding="UTF-8") as al:
        al.writelines(anal)


def count_freq(f):
    with open(f, 'r', encoding='UTF-8') as inp:
        data = inp.readlines()

    dictionary = dict()

    for word in data:
        word = word.replace("\n", "").replace(" ", "")
        for char in word:
            if char not in dictionary.keys():
                dictionary[char] = 1
            else:
                dictionary[char] += 1

    print(dictionary)
    print(sorted(dictionary, key=dictionary.get, reverse=True))


count_freq("ch_dev.txt")
#compare("original_5_dev_12000.txt", "original_bs_dev_12000.txt")
#compare("original_bs_dev_12000.txt", "original_5_dev_12000.txt")
