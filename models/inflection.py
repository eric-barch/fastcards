class Inflection:
    def __init__(self, inflection):
        self.inflection = inflection
        self.notes = []

    def add_note(self, note):
        if note.source != self.inflection:
            raise NoteInflectionMismatchException(note, self)
        self.notes.append(note)

    def __str__(self):
        return self.inflection

    def __format__(self, format_spec):
        return format(str(self), format_spec)


class NoteInflectionMismatchException(Exception):
    def __init__(self, note, inflection):
        super().__init__(
            f"Note {note.source} does not match Inflection {inflection.inflection}"
        )
