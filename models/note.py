class Note:
    def __init__(self, pos, source, target, id=None):
        self.id = id
        self.pos = pos
        self.source = source
        self.target = target
        self.will_add = False

    def __str__(self):
        return f"{self.id + ' ' if self.id else ''}{self.source} ({self.pos}): {self.target} {self.will_add}"


class InflectedNote(Note):
    def __init__(self, pos, source, target, gender, number, id=None):
        super().__init__(pos, source, target, id)
        self.gender = gender
        self.number = number

    def __str__(self):
        return f"{self.id + ' ' if self.id else ''}{self.source} ({self.pos}, {self.gender}, {self.number}): {self.target} {self.will_add}"
