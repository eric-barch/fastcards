from global_vars import column_widths
from models.potential_note import PotentialNote


class Token:
    def __init__(self, text, lemma, pos, start, end):
        self.text = PotentialNote(text)
        self.lemma = PotentialNote(lemma)
        self.pos = pos
        self.start = start
        self.end = end

    def __str__(self):
        return (
            f"{self.text.text:<{column_widths[0]}}"
            f"{self.text.source:<{column_widths[1]}}"
            f"{self.text.target:<{column_widths[2]}}"
            f"{self.lemma.text:<{column_widths[3]}}"
            f"{self.lemma.source:<{column_widths[4]}}"
            f"{self.lemma.target:<{column_widths[5]}}"
            f"{self.pos:<{column_widths[6]}}"
        )
