class Person:
    def __init__(self, name):
        self.name = name
        self.contents = []

    def __str__(self):
        return self.name

    def logtime(self, time):
        for item in self.contents:
            if time in item.time:
                print(item)

    def logword(self, phrase):
        for item in self.contents:
            if phrase in item.words:
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

def cparse(filename):
    players = []
    newfile = open(filename,'r',encoding='utf-16')
    for line in newfile:
        line = line.strip().split('\t')
