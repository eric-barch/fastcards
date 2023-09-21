from .note.note import Note


class Token:
    def __init__(self, text, spacy_token, openai_token):
        self.text = text
        self.spacy_token = spacy_token
        self.openai_token = openai_token

        self.representation = self.spacy_token.representation
        self.source = self.openai_token.source
        self.target = self.openai_token.target
        self.pos = self.openai_token.pos
        self.gender = self.openai_token.gender
        self.number = self.openai_token.number

        self.note = Note(self)

    def __repr__(self, number, indent, column_width, row_labels):
        lines = []

        for row_label in row_labels:
            values = [
                str(getattr(self.spacy_token, row_label, "None")),
                str(getattr(self.openai_token, row_label, "None")),
                str(getattr(self, row_label, "None")),
            ]

            line = f"{'':<{indent}}{row_label + ':':<{column_width}}{values[0]:<{column_width}}{values[1]:<{column_width}}{values[2]}"
            lines.append(line)

        number_string = f"{number}."

        lines[0] = number_string + lines[0][len(number_string) :]

        return f"{lines[0]}\n" + "\n".join(lines[1:])
