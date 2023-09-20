class SpacyToken:
    def __init__(self, representation, start, end, lemma, pos, gender, number):
        self.representation = representation
        self.start = start
        self.end = end
        self.lemma = lemma
        self.pos = pos
        self.gender = gender
        self.number = number
