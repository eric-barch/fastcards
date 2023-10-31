class Note:
    def __init__(self, id, source, target):
        self.id = id
        self.source = source
        self.target = target

    def __str__(self):
        return f"{self.id} {self.source}: {self.target}"
