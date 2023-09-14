import json
import spacy

from .potential_note import PotentialNote

nlp = spacy.load("fr_core_news_sm")


class PotentialNoteList(list):
    def __init__(self, session, french_string):
        super().__init__()
        self.session = session
        self.french_string = french_string

        self.tokens = self.generate_tokens(self.french_string)
        print(f"\ntokens: {json.dumps(self.tokens, indent=4)}")

        request_tokens = self.generate_request_tokens()
        request = json.dumps(
            {
                "string": self.french_string,
                "tokens": request_tokens,
            },
            indent=4,
        )
        print(f"\nrequest: {request}")

        response = self.session.openai_interface.confirm_tokens(request)
        print(f"\nresponse: {json.dumps(response, indent=4)}")

        # self.create_potential_notes()

    def generate_tokens(self, french_string):
        string = nlp(french_string)

        token_data = []

        for token in string:
            if token.pos_ != "PUNCT":
                note_front = self.determine_note_front(token)

                morph = token.morph.to_dict()

                gender_abbr = morph.get("Gender")
                gender = self.get_gender_string(gender_abbr) if gender_abbr else None

                number_abbr = morph.get("Number")
                number = self.get_number_string(number_abbr) if number_abbr else None

                token_datum = {
                    "note_front": note_front,
                    "representation": token.text,
                    "start": token.idx,
                    "end": token.idx + len(token.text),
                    "lemma": token.lemma_,
                    "pos": self.get_pos_string(token.pos_),
                    "gender": gender,
                    "number": number,
                }

                token_data.append(token_datum)

        return token_data

    def determine_note_front(self, token):
        is_contraction_part = token.text.endswith("'")
        is_inverted_subject_pron = token.text.startswith("-")
        is_verb = self.get_pos_string(token.pos_) == "verb"

        lemma_front = is_contraction_part or is_inverted_subject_pron or is_verb

        if lemma_front:
            return token.lemma_

        return token.text

    def generate_request_tokens(self):
        request_token_data = []

        for token_datum in self.tokens:
            request_token_datum = {
                "representation": token_datum["representation"],
                "note_front": token_datum["note_front"],
                "pos": token_datum["pos"],
            }
            request_token_data.append(request_token_datum)

        return request_token_data

    def get_pos_string(self, abbreviation):
        pos = {
            "ADJ": "adjective",
            "ADP": "adposition",
            "ADV": "adverb",
            "AUX": "auxiliary",
            "CONJ": "conjunction",
            "CCONJ": "coord conj",
            "DET": "determiner",
            "INTJ": "interjection",
            "NOUN": "noun",
            "NUM": "numeral",
            "PART": "particle",
            "PRON": "pronoun",
            "PROPN": "proper noun",
            "PUNCT": "punctuation",
            "SCONJ": "subord conj",
            "SYM": "symbol",
            "VERB": "verb",
            "X": "other",
            "SPACE": "space",
        }
        return pos[abbreviation.upper()]

    def get_gender_string(self, abbreviation):
        gender = {
            "MASC": "masculine",
            "FEM": "feminine",
            "NEUT": "neuter",
        }
        return gender[abbreviation.upper()]

    def get_number_string(self, abbreviation):
        number = {
            "SING": "singular",
            "PLUR": "plural",
        }
        return number[abbreviation.upper()]

    def create_potential_notes(self):
        for token_datum in self.tokens:
            potential_note = PotentialNote(
                self.session, self.french_string, token_datum
            )
            self.append(potential_note)
