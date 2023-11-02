from global_vars import column_widths


class Token:
    def __init__(self, text, lemma, pos, start, end):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.start = start
        self.end = end
        self.notes = []
        self.marked_for_lookup = False

    def add_note(self, new_note):
        if not any(existing_note.id == new_note.id for existing_note in self.notes):
            self.notes.append(new_note)

    def __str__(self):
        return (
            f"{self.text:<{column_widths[0]}}"
            f"{self.lemma:<{column_widths[1]}}"
            f"{self.pos:<{column_widths[2]}}"
            f"{'marked' if self.marked_for_lookup else '':<{column_widths[3]}}"
            f"[{', '.join(str(note) for note in self.notes)}]"
        )
