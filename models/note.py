class Note:
    def __init__(self, pos, source, target, id=None, gender=None, number=None):
        self.pos = pos
        self.source = source
        self.target = target
        self.id = id
        self.gender = gender
        self.number = number
        self.will_add = False

    def __str__(self):
        return (
            f"{self.source:<15}"
            + f"{self.target:<15}"
            + f"{self.pos:<10}"
            + f"{self.gender if self.gender else 'None':<10}"
            + f"{self.number if self.number else 'None':<10}"
        )
