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
        return '[{}][{}]: {}'.format(self.toon, self.time, self.contents)

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

    def psearch(self, pname, query):
        #searches for player and surround text
        if pname in self.names:
            index = self.names.index(pname)
            results = self.splayers[index].logword2(query)
            if results = []:
                print('Phrase not found')
            for log in results:
                timetup = timezip(log)

def timezip(obj):
    """(Chat obj) -> tuple of strs

    >>>timezip('00:00:00')
    ('23:55:00', '00:05:00')
    """
    time = log.obj.split(':')
    
    for index, numeral in enumerate(time):
        time[index] = int(numeral)
    
    time2 = time[:]
    time[1] -= 5
    time2[1] += 5

    if time[1] < 0:
        time[0] -= 1
        time[1] += 60
        if time[0] < 0:
            time[0] += 24
    
    if time2[1] > 60:
        time2[0] += 1
        time2[1] -= 60
        if time2[0] > 24:
            time2[0] -= 24

    newtime1 = ''
    newtime2 = ''

    for numeral in time:
        newtime1 += '{}:'.format(numeral)
    newtime1 = newtime1[:-1]

    for numeral in time2:
        newtime2 += '{}:'.format(numeral)
    newtime2 = newtime2[:-1]

    return newtime1, newtime2



if __name__ == '__main__':
    var = Speech('ChatLog20150125_00.txt')
    var.order()