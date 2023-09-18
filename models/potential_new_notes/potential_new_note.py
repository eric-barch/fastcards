class PotentialNote:
    def __init__(self, session, string, token):
        self.session = session
        self.string = string
        self.front = token["note_front"]
        self.back = token["note_back"]
        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.pos = token["pos"]
        self.gender = token["gender"]
        self.number = token["number"]
        self.already_exists = self.check_if_already_exists()

    def __repr__(self):
        front = f"front: {self.front}"
        back = f"back: {self.back}"
        already_exists = f"already_exists: {self.already_exists}"

        return f"{front:<30}{back:<30}{already_exists}"

    def check_if_already_exists(self):
        existing_notes = self.session.anki_interface.find_notes_by_front(
            self.front,
        )

        if existing_notes:
            self.already_exists = True
        else:
            self.already_exists = False

        return self.already_exists
