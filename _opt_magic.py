OPT_LOCATION = 'C:/Games/Rappelz/rappelz_v1.opt'
NICKNAME = 'Greed'
if __name__ == '__main__':
    file = open(OPT_LOCATION, 'r')
    startWrite = False
    l = []
    for line in file:
        if line == '[' + NICKNAME + ']\n':
            print(line)
            startWrite = True;
            continue
        if startWrite:
            l.append(line)
        if line[0] == '[':
            startWrite = False
    file.close()
    for line in l:
        print(line)
