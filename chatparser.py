class Person:
    def __init__(self, name):
        self.name = name
        self.contents = []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if (self.name) == (other.name):
            return True

    def logtime(self, time):
        for item in self.contents:
            if time in item.time:
                print(item)

    def logword(self, phrase):
        for item in self.contents:
            if phrase in item.contents:
                print(item)

    def logtype(self, category):
        for item in self.contents:
            if item.category == category.lower().title():
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
        return '[{}]: {}'.format(self.toon, self.contents)

def cparse(filename):
    players = []
    newfile = open(filename,'r',encoding='utf-16')
    for line in newfile:
        line = line.strip().split('\t')
        newtext = Chat(line)
        temp = Person(line[4])
        
        if temp in players:
            players[players.index(temp)].add(newtext)
        
        elif temp not in players:
            players.append(temp)
            players[players.index(temp)].add(newtext)

    return players

if __name__ == '__main__':
    var = cparse('ChatLog20140826_00.txt')
    for item in var:
        print(item)
    len(var)