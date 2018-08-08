import sys

if __name__ == '__main__':
    t_steps = sys.argv[1]     
    with open("cer.txt", 'r', encoding='UTF-8') as inp:
       lines = inp.readlines()
    with open("cer-clean.txt", 'w+', encoding='UTF-8') as out:
       steps = list(range(int(t_steps)-900, int(t_steps)+1, 100))
       i = 0
       for line in lines:
          if "WER" in line:
             line = line.replace("WER", "CER")
             out.write(line)
             out.write(str(steps[i]) + '\n')
             i += 1
         
          
       
