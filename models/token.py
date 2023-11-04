class Token:
    def __init__(self, text, lemma, pos, start, end):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.start = start
        self.end = end
        self.notes = []
        self.will_look_up = False

    def add_note(self, new_note):
        if not any(existing_note.id == new_note.id for existing_note in self.notes):
            self.notes.append(new_note)

    def __str__(self):
        targets = []

        for note in self.notes:
            if note.source == self.text:
                targets.append(note.target)
            else:
                targets.append(f"{note.target} ({note.source})")

        return (
            f"{self.text:<15}"
            f"{self.lemma:<15}"
            f"{self.pos:<10}"
            f"{', '.join(targets)}"
        )
