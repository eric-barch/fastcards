class Token:
    def __init__(self, session, spacy_token, openai_token):
        self.session = session

        self.spacy_token = spacy_token
        self.openai_token = openai_token

        self.representation = self.spacy_token.representation
        self.source = self.openai_token.source
        self.target = self.openai_token.target
        self.pos = self.openai_token.pos
        self.gender = self.openai_token.gender
        self.number = self.openai_token.number

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

    def get_pos_source_and_target(self):
        pos_target_to_source = {
            "adjective": "adjectif",
            "adposition": "adposition",
            "adverb": "adverbe",
            "auxiliary": "auxiliaire",
            "conjunction": "conjonction",
            "coord conj": "conj de coord",
            "determiner": "déterminant",
            "interjection": "interjection",
            "noun": "nom",
            "numeral": "numéral",
            "particle": "particule",
            "preposition": "préposition",
            "pronoun": "pronom",
            "proper noun": "nom propre",
            "punctuation": "ponctuation",
            "subord conj": "conj de subord",
            "symbol": "symbole",
            "verb": "verbe",
            "other": "autre",
            "space": "espace",
        }

        pos_target = self.token["pos"]

        if not pos_target:
            return "none", "none"

        pos_source = pos_target_to_source[pos_target]
        return pos_source, pos_target

    def get_gender_source_and_target(self):
        gender_target_to_source = {
            "masculine": "masculin",
            "feminine": "féminin",
            "neuter": "neutre",
        }

        gender_target = self.token["gender"]

        if not gender_target:
            return "none", "none"

        gender_source = gender_target_to_source[gender_target]
        return gender_source, gender_target

    def get_number_source_and_target(self):
        number_target_to_source = {
            "singular": "singulier",
            "plural": "pluriel",
        }

        number_target = self.token["number"]

        if not number_target:
            return "none", "none"

        number_source = number_target_to_source[number_target]
        return number_source, number_target

    def check_if_exists(self):
        matching_notes = self.session.anki.find_notes(
            self.source,
        )

        if matching_notes:
            self.exists = True
        else:
            self.exists = False

        return self.exists
