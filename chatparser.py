class Person:
    def __init__(self, name):
        self.name = name
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
                newtext = Chat(line)
                temp = Person(line[4])
                self.total.append(newtext)
                if temp in players:
                    players[players.index(temp)].add(newtext)
                
                elif temp not in players:
                    players.append(temp)
                    self.names.append(line[4])
                    players[players.index(temp)].add(newtext)
        self.players = players[:]
        players.sort()
        self.names.sort()
        self.splayers = players

    def __str__(self):
        names = ''
        for item in self.splayers:
            names += '{}\n'.format(str(item))

        return names

    def disp(self):
        x = 0
        for item in self.players:
            print('{}: {}'.format(x, str(item)))
            x += 1

    def order(self):
        x = 0
        for item in self.splayers:
            print('{}: {}'.format(x, str(item)))
            x += 1

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
                while self.total[cur].time > timetup[0] and len(rez) < 1 + msgs:
                    rez.append(self.total[cur])
                    cur -= 1
                cur = mid + 1
                while self.total[cur].time < timetup[1] and len(rez) < 1 + 2 * msgs:
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



if __name__ == '__main__':
    var = Speech('ChatLog20150125_00.txt')
    var.order()
    while True:
        examine = input('#, phrase: ').split(',')
        for index, item in enumerate(examine):
            examine[index] = item.strip()
        var.psearch(var.splayers[int(examine[0])].name, examine[1])