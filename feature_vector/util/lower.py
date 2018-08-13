import os


def lower_everything(eng_file):
    with open(eng_file, 'r', encoding='UTF-8-sig') as ip:
        lines = [line.lower() for line in ip.readlines()]
        print(lines)
    with open('../' + eng_file, 'w+', encoding='UTF-8') as output:
        output.writelines(lines)


def check_same(file1, file2):
    with open(file1, 'r', encoding='UTF-8') as f1:
        d1 = f1.readlines()

    with open(file2, 'r', encoding='UTF-8') as f2:
        d2 = f2.readlines()

    assert len(d1) == len(d2)
    same = 0
    for i in range(len(d1)):
        if d1[i] == d2[i]:
            same += 1

    print(str(same / len(d1)) + "% is the same")
