class Note:
    def __init__(self, session, source, token):
        self.session = session
        self.source = source
        self.front = token["front"]
        self.back = token["back"]
        self.pos = token["pos"]
        self.gender = token["gender"]
        self.number = token["number"]
        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.already_exists = self.check_if_already_exists()

    def __repr__(self):
        front = f"front: {self.front}"
        back = f"back: {self.back}"
        pos = f"pos: {self.pos}"
        gender = f"gender: {self.gender}"
        number = f"number: {self.number}"
        already_exists = f"already_exists: {self.already_exists}"
        spacer = f"\n{'':<5}"

        return f"{front}{spacer}{back}{spacer}{pos}{spacer}{gender}{spacer}{number}{spacer}{already_exists}"

    def check_if_already_exists(self):
        existing_notes = self.session.anki.find_notes_by_front(
            self.front,
        )

        if existing_notes:
            self.already_exists = True
        else:
            self.already_exists = False

        return self.already_exists
