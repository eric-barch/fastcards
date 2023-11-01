from global_vars import column_widths


class Token:
    def __init__(self, text, lemma, pos, start, end):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.start = start
        self.end = end
        self.existing_notes = []
        self.marked_for_lookup = False

    def add_existing_note(self, existing_note):
        if not any(note.id == existing_note.id for note in self.existing_notes):
            self.existing_notes.append(existing_note)

    def __str__(self):
        return (
            f"{self.text:<{column_widths[0]}}"
            f"{self.lemma:<{column_widths[1]}}"
            f"{self.pos:<{column_widths[2]}}"
            f"{'marked' if self.marked_for_lookup else '':<{column_widths[3]}}"
            f"[{', '.join(str(note) for note in self.existing_notes)}]"
        )
