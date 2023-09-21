class Note:
    def __init__(self, token):
        self.source = token.source
        self.target = token.target
        self.pos_source, self.pos_target = self.get_pos_source_and_target(token.pos)
        self.gender_source, self.gender_target = self.get_gender_source_and_target(
            token.gender
        )
        self.number_source, self.gender_target = self.get_number_source_and_target(
            token.number
        )

    def get_pos_source_and_target(self, pos_target):
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

        if not pos_target:
            return "aucun", "none"

        pos_source = pos_target_to_source[pos_target]
        return pos_source, pos_target

    def get_gender_source_and_target(self, gender_target):
        gender_target_to_source = {
            "masculine": "masculin",
            "feminine": "féminin",
            "neuter": "neutre",
        }

        if not gender_target:
            return "aucun", "none"

        gender_source = gender_target_to_source[gender_target]
        return gender_source, gender_target

    def get_number_source_and_target(self, number_target):
        number_target_to_source = {
            "singular": "singulier",
            "plural": "pluriel",
        }

        if not number_target:
            return "aucun", "none"

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
