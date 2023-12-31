class Inflection:
    def __init__(self, string):
        self.string = string
        self.notes = []

    def add_note(self, note):
        if note.source.strip().lower() != self.string.strip().lower():
            raise NoteInflectionMismatchException(note, self)
        self.notes.append(note)

    def __str__(self):
        return self.string

    def __format__(self, format_spec):
        return format(str(self), format_spec)


class NoteInflectionMismatchException(Exception):
    def __init__(self, note, inflection):
        super().__init__(
            f"Note {note.source} does not match Inflection {inflection.string}"
        )
