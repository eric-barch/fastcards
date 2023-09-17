class PotentialNote:
    def __init__(self, session, string, token):
        self.session = session
        self.string = string
        self.note_front = token["note_front"]
        self.english = token["english"]
        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.pos = token["pos"]
        self.gender = token["gender"]
        self.number = token["number"]
        self.exists_in_anki = False

    def __repr__(self):
        front = f"front: {self.note_front}"
        english = f"english: {self.english}"
        exists_in_anki = f"exists_in_anki: {self.exists_in_anki}"

        return f"{front:<30}{english:<30}{exists_in_anki}"
