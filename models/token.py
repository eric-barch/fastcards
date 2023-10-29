from models.potential_note import PotentialNote


class Token:
    def __init__(self, representation_text, lemma_text, start, end):
        self.representation = PotentialNote(representation_text)
        self.lemma = PotentialNote(lemma_text)
        self.start = start
        self.end = end
