from models.inflection import Inflection, NoteInflectionMismatchException


class Token:
    def __init__(self, text, lemma, pos, start, end):
        self.text = Inflection(text)
        self.lemma = Inflection(lemma)
        self.pos = pos
        self.start = start
        self.end = end
        self.will_look_up = False

    def get_inflection_strings(self):
        return [str(self.text).strip().lower(), str(self.lemma).strip().lower()]

    def add_note(self, note):
        for inflection in [self.text, self.lemma]:
            try:
                inflection.add_note(note)
                return
            except NoteInflectionMismatchException:
                continue

        # if the above fails, spaCy incorrectly detected token's lemma. replace it and add note.
        self.lemma = Inflection(note.source)
        self.lemma.add_note(note)

        self.will_look_up = False

    def get_notes(self):
        notes = []

        for inflection in [self.text, self.lemma]:
            notes.extend(inflection.notes)

        return notes

    def __str__(self):
        targets = []

        if self.text.notes:
            targets = [note.target for note in self.text.notes]
        elif self.lemma.notes:
            targets = [f"{note.target} ({note.source})" for note in self.lemma.notes]

        return (
            f"{self.text:<15}"
            f"{self.lemma:<15}"
            f"{self.pos:<10}"
            f"{', '.join(targets)}"
        )


class NoteTokenMismatchException(Exception):
    def __init__(self, note, token):
        super().__init__(f"Note {note.source} does not match Token {token.text}")
