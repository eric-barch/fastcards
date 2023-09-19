class Note:
    def __init__(self, session, token):
        self.session = session
        self.token = token
        self.source = self.token["source"]
        self.target = self.token["target"]
        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.already_exists = self.check_for_existing()

        self.pos_source, self.pos_target = self.get_pos_source_and_target()
        self.gender_source, self.gender_target = self.get_gender_source_and_target()
        self.number_source, self.number_target = self.get_number_source_and_target()

    def __repr__(self):
        indent = 5
        column_width = 30

        parts = [
            f"source: {self.source:<{22}}target: {self.target}",
            f"{'':<{indent}}{'pos_source: ' + self.pos_source:<{column_width}}pos_target: {self.pos_target}",
            f"{'':<{indent}}{'gender_source: ' + self.gender_source:<{column_width}}gender_target: {self.gender_target}",
            f"{'':<{indent}}{'number_source: ' + self.number_source:<{column_width}}number_target: {self.number_target}",
            f"{'':<{indent}}{'already_exists: ' + str(self.already_exists)}",
        ]

        return "\n".join(parts)

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

    def check_for_existing(self):
        existing_notes = self.session.anki.find_notes(
            self.source,
        )

        if existing_notes:
            self.already_exists = True
        else:
            self.already_exists = False

        return self.already_exists
