class Note:
    def __init__(self, session, token):
        self.session = session
        self.token = token
        self.source = self.token["source"]
        self.target = self.token["target"]

        self.pos_source, self.pos_target = self.get_pos()
        self.gender_source, self.gender_target = self.get_gender()
        self.number_source, self.number_target = self.get_number()

        self.representation = token["representation"]
        self.start = token["start"]
        self.end = token["end"]
        self.lemma = token["lemma"]
        self.already_exists = self.check_if_already_exists()

    def __repr__(self):
        front = f"front: {self.source}"
        back = f"back: {self.target}"
        pos = f"pos: {self.pos_source}"
        gender = f"gender: {self.gender_target}"
        number = f"number: {self.number_target}"
        already_exists = f"already_exists: {self.already_exists}"
        spacer = f"\n{'':<5}"

        # TODO: Hate this
        return f"{front}{spacer}{back}{spacer}{pos}{spacer}{gender}{spacer}{number}{spacer}{already_exists}"

    def get_pos(self):
        pos_sources = {
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
        if pos_target:
            pos_source = pos_sources[pos_target]
        else:
            pos_source = None

        return pos_source, pos_target

    def get_gender(self):
        gender_sources = {
            "masculine": "masculin",
            "feminine": "féminin",
            "neuter": "neutre",
        }

        gender_target = self.token["gender"]
        if gender_target:
            gender_source = gender_sources[gender_target]
        else:
            gender_source = None

        return gender_source, gender_target

    def get_number(self):
        number_sources = {
            "singular": "singulier",
            "plural": "pluriel",
        }

        number_target = self.token["number"]
        if number_target:
            number_source = number_sources[number_target]
        else:
            number_source = None

        return number_source, number_target

    def check_if_already_exists(self):
        existing_notes = self.session.anki.find_notes_by_front(
            self.source,
        )

        if existing_notes:
            self.already_exists = True
        else:
            self.already_exists = False

        return self.already_exists
