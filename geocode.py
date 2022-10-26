class Geocode:
    def __init__(self):
        self.names_list = []
        with open('cities15000.txt', 'r', encoding='utf-8') as codes:
            for line in codes:
                name = line[:-1].split('\t')
                dname = (name[2], tuple(name[3].split(',')), name[4], name[5])
                self.names_list.append(dname)

    def find(self, name):
        for names in self.names_list:
            if name.upper() == names[0].upper() or name in names[1]:
                return (names[0], names[2], names[3])
        return None

