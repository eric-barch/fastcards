import json

import spacy

from .note.spacy_token.spacy_token import SpacyToken
from .note.note import Note

nlp = spacy.load("fr_core_news_sm")


class Notes(list):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.text = session.text
        self.text.notes = self
        self.spacy_tokens = self.get_spacy_tokens()
        self.openai_tokens = self.get_openai_tokens()
        self.create_notes()

    def __repr__(self):
        repr = "\n"

        for i, note in enumerate(self):
            number = f"\n{i + 1}."
            repr += f"{number:<6}{note}"

            if i != len(self) - 1:
                repr += "\n"

        return repr

    def get_spacy_tokens(self):
        parsed_string = nlp(self.source)

        spacy_tokens = []

        for token in parsed_string:
            if token.pos_ != "PUNCT":
                morph = token.morph.to_dict()

                gender_abbr = morph.get("Gender")
                gender = self.get_gender_string(gender_abbr) if gender_abbr else None

                number_abbr = morph.get("Number")
                number = self.get_number_string(number_abbr) if number_abbr else None

                spacy_token = SpacyToken(
                    token.text,
                    token.idx,
                    token.idx + len(token.text),
                    token.lemma,
                    token.pos,
                    gender,
                    number,
                )

                spacy_tokens.append(spacy_token)

        return spacy_tokens

    def get_source(self, token):
        is_contraction_part = token.text.endswith("'")
        is_inverted_subject_pron = token.text.startswith("-")
        is_verb = self.get_pos_string(token.pos_) == "verb"
        is_proper_noun = self.get_pos_string(token.pos_) == "proper noun"

        lemma_front = is_contraction_part or is_inverted_subject_pron or is_verb

        if lemma_front:
            front = token.lemma_
        else:
            front = token.text

        if is_proper_noun:
            return front.capitalize()
        else:
            return front.lower()

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

    def get_request_tokens(self, parsed_tokens):
        request_tokens = []

        for token in parsed_tokens:
            request_token = {
                "representation": token["representation"],
                "source": token["source"],
                "pos": token["pos"],
                "gender": token["gender"],
                "number": token["number"],
            }
            request_tokens.append(request_token)

        return request_tokens

    def set_tokens(self, parsed_tokens, confirmed_tokens):
        if len(parsed_tokens) != len(confirmed_tokens):
            raise Exception(
                "parsed_tokens and confirmed_tokens must be the same length"
            )

        tokens = parsed_tokens

        for i, token in enumerate(tokens):
            confirmed_token = confirmed_tokens[i]

            token["source"] = confirmed_token["source"]
            token["target"] = confirmed_token["target"]
            token["pos"] = confirmed_token["pos"]
            token["gender"] = confirmed_token["gender"]
            token["number"] = confirmed_token["number"]

        self.tokens = tokens
        return self.tokens

    def create_notes(self):
        for token in self.tokens:
            note = Note(
                self.session,
                token,
            )
            self.append(note)

        return self