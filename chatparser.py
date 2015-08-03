from os import listdir

class Person:
    def __init__(self, name, ident):
        self.name = name
        self.ident = ident
        self.contents = []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if (self.name) == (other.name):
            return True

    def __lt__(self, other):
        if (self.name) < (other.name):
            return True

    def __gt__(self, other):
        if (self.name) > (other.name):
            return True
    def __len__(self):
        return len(self.contents)

    def logtime(self, time):
        for item in self.contents:
            if time in item.time:
                print(item)

    def logword(self, phrase):
        for item in self.contents:
            if phrase in item.contents:
                print(item)

    def logword2(self, phrase):
        fodder = []
        for item in self.contents:
            if phrase in item.contents:
                fodder.append(item)
        return fodder

    def logtype(self, category):
        for item in self.contents:
            if item.category == category.upper():
                print(item)

    def loghybrid(self, time=None, category=None, phrase=None):
        pass

    def add(self, item):
        self.contents.append(item)


class Chat:
    def __init__(self, items):
        self.time = items[0][11:]
        self.contents = items[-1]
        self.category = items[2]
        self.ident = items[3]
        self.toon = items[4]

    def __str__(self):
        return '[{}][{}]: {}'.format(self.time, self.toon, self.contents)

    def __eq__(self, other):
        if self.time == other.time:
            return True

    def __lt__(self, other):
        if self.time < other.time:
            return True

    def __gt__(self, other):
        if self.time > other.time:
            return True


class Speech:
    def __init__(self, filename):
        players = []
        self.total = []
        self.names = []
        with open(filename,'r',encoding='utf-16') as newfile:
            for line in newfile:
                line = line.strip().split('\t')
                if len(line) < 6:
                    continue

                newtext = Chat(line)
                temp = Person(line[4], line[3])
                self.total.append(newtext)
                if temp in players:
                    players[players.index(temp)].add(newtext)
                
                elif temp not in players:
                    players.append(temp)
                    self.names.append(line[4])
                    players[players.index(temp)].add(newtext)
        players.sort()
        self.names.sort()
        self.splayers = players

    def __str__(self):
        names = ''
        for item in self.splayers:
            names += '{}\n'.format(str(item))

        return names

    def filler(self, filename):
        players = []
        self.total = []
        self.names = []
        with open(filename,'r',encoding='utf-16') as newfile:
            for line in newfile:
                line = line.strip().split('\t')
                newtext = Chat(line)
                self.total.append(newtext)
                temp = Person(line[4], line[3])
                temp2 = [line[3]]
                if temp.ident in players:
                    players[players.index(temp)].add(newtext)
                
                elif temp not in players:
                    players.append(temp)
                    self.names.append(line[4])
                    players[players.index(temp)].add(newtext)
        players.sort()
        self.splayers = players

    def newstr(self):
    	pass

    def order(self):
        for index, item in enumerate(self.splayers):
            print('{}: {}'.format(index, str(item)))

    def psearch(self, pname, query, interval=5, msgs=5):
        #searches for player and surround text
        if pname in self.names:
            index = self.names.index(pname)
            results = self.splayers[index].logword2(query)
            if results == []:
                print('Phrase not found')
            for log in results:
                timetup = timezip(log, 5)
                mid = self.total.index(log)
                cur = mid
                rez = []
                while self.total[cur].time >= timetup[0] and len(rez) < 1 + msgs:
                    if self.total[cur].category == log.category:
                        rez.append(self.total[cur])
                    cur -= 1
                cur = mid + 1
                while self.total[cur].time <= timetup[1] and len(rez) < 1 + 2 * msgs:
                    if self.total[cur].category == log.category:
                        rez.append(self.total[cur])
                    cur += 1
                rez.sort()

                for item in rez:
                    print(str(item))
                print('==============')



def timezip(obj, interval):
    """(Chat obj) -> tuple of strs

    >>>timezip('00:00:00')
    ('23:55:00', '00:05:00')
    """
    try:
        time = obj.time.split(':')
    except AttributeError:
        time = obj.split(':')
    for index, numeral in enumerate(time):
        time[index] = int(numeral)
    
    time2 = time[:]
    time[1] -= interval
    time2[1] += interval

    if time[1] < 0:
        time[0] -= 1
        time[1] += 60
        if time[0] < 0:
            time[0] += 24
    
    if time2[1] >= 60:
        time2[0] += 1
        time2[1] -= 60
        if time2[0] > 24:
            time2[0] -= 24

    newtime1 = ''
    newtime2 = ''

    for numeral in time:
        if len(str(numeral)) == 1:
            newtime1 += '0{}:'.format(numeral)
        else:
            newtime1 += '{}:'.format(numeral)
    newtime1 = newtime1[:-1]

    for numeral in time2:
        if len(str(numeral)) == 1:
            newtime2 += '0{}:'.format(numeral)
        else:
            newtime2 += '{}:'.format(numeral)
    newtime2 = newtime2[:-1]

    return newtime1, newtime2


def seperate_chat():            
    answer = input('Extract: \n[T]eam, [P]arty, Pu[B]lic, [W]hispers, [A]ll: ').lower()
    work = open(some_files[int(file_num)], 'r', encoding='utf-16')
    if answer == 't':
        team = open(some_files[int(file_num)][:-4] + '_TeamOnly.txt','w', encoding='utf-16')
    elif answer == 'p':
        party = open(some_files[int(file_num)][:-4] + '_PartyOnly.txt','w', encoding='utf-16')
    elif answer == 'w':
        whisper = open(some_files[int(file_num)][:-4] + '_WhisperOnly.txt','w', encoding='utf-16')
    elif answer == 'b':
        public = open(some_files[int(file_num)][:-4] + '_PublicOnly.txt','w', encoding='utf-16')
    else:
        team = open(some_files[int(file_num)][:-4] + '_TeamOnly.txt','w', encoding='utf-16')
        party = open(some_files[int(file_num)][:-4] + '_PartyOnly.txt','w', encoding='utf-16')
        whisper = open(some_files[int(file_num)][:-4] + '_WhisperOnly.txt','w', encoding='utf-16')
        public = open(some_files[int(file_num)][:-4] + '_PublicOnly.txt','w', encoding='utf-16')
    for line in work:
        newline = line.split('\t')
        if newline[2] == 'GUILD' and (answer == 'a' or answer == 't'):
            team.write(line)
        elif newline[2] == 'PARTY' and (answer == 'a' or answer == 'p'):
            party.write(line)
        elif newline[2] == 'REPLY' and (answer == 'a' or answer == 'w'):
            whisper.write(line)
        elif newline[2] == 'PUBLIC' and (answer == 'a' or answer == 'b'):
            public.write(line)

if __name__ == '__main__':
    all_files = listdir()
    some_files = []
    for item in all_files:
        if 'ChatLog' in item:
            some_files.append(item)
    for index, item in enumerate(some_files):
        print('{}: {}/{}/{}'.format(index, item[11:13], item[13:15], item[7:11]))

    file_num = input('Log #: ')
    while True:
        answer = input('Se[A]rch or Se[P]erate?: ').lower()
        if answer == 'a':
            var = Speech(some_files[int(file_num)])
            var.order()
            examine = input('#, phrase: ').split(',')
            for index, item in enumerate(examine):
                examine[index] = item.strip()
            var.psearch(var.splayers[int(examine[0])].name, examine[1])
        else:
            seperate_chat()
            break
