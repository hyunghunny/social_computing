# coding=UTF-8

class TSVDataLoader :
    def __init__(self, fileName) :

        self.lines = [line for line in file(fileName)]

        # First line is the column titles
        words = self.lines[0].strip().split('\t')[1:]
        #print(words)
        self.names = []
        self.data = []
        for line in self.lines[1:]:
            p = line.strip().split('\t')
            # First column in each row is the rowname
            self.names.append(p[0])
            # The data for this row is the remainder of the row
            self.data.append([float(x) for x in p[1:]])