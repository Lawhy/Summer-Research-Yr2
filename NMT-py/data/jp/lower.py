import os


def lower_everything(eng_file):
    with open(eng_file, 'r', encoding='UTF-8-sig') as ip:
        lines = [line.lower() for line in ip.readlines()]
        print(lines)
    with open('../' + eng_file, 'w+', encoding='UTF-8') as output:
        output.writelines(lines)


def to_windows(file):
    with open(file, 'r', encoding='UTF-8-sig') as ip:
        lines = ip.readlines()
        print(len(lines))
    with open('../' + file, 'w+', encoding='UTF-8') as output:
        output.writelines(lines)


for file in os.listdir('.'):
    to_windows(file)