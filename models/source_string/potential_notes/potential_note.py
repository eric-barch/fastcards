class PotentialNote:
    def __init__(self, session, string, token):
        self.session = session
        self.string = string
        self.note_front = token["note_front"]
        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.pos = token["pos"]
        self.gender = token["gender"]
        self.number = token["number"]
