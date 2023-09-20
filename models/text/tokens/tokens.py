import json

import spacy

from .token.spacy_token import SpacyToken
from .token.openai_token import OpenAiToken

nlp = spacy.load("fr_core_news_sm")


class Tokens(list):
    def __init__(self, session):
        super().__init__()
        self.session = session

        self.text = session.text
        self.text.notes = self

        spacy_tokens = self.get_spacy_tokens()
        openai_tokens = self.get_openai_tokens(spacy_tokens)

        # self.create_tokens(spacy_tokens, openai_tokens)

    def __repr__(self):
        repr = "\n"

        for i, token in enumerate(self):
            number = f"\n{i + 1}."
            repr += f"{number:<6}{token}"

            if i != len(self) - 1:
                repr += "\n"

        return repr

    def get_spacy_tokens(self):
        source = self.text.source

        parsed_objects = nlp(source)

        spacy_tokens = []

        for parsed_object in parsed_objects:
            if parsed_object.pos_ == "PUNCT":
                continue

            pos = self.get_pos_string(parsed_object.pos_)

            morph = parsed_object.morph.to_dict()

            gender_abbr = morph.get("Gender")
            gender = self.get_gender_string(gender_abbr) if gender_abbr else None

            number_abbr = morph.get("Number")
            number = self.get_number_string(number_abbr) if number_abbr else None

            spacy_token = SpacyToken(
                parsed_object.text,
                self.get_source(parsed_object),
                parsed_object.idx,
                parsed_object.idx + len(parsed_object.text),
                parsed_object.lemma,
                pos,
                gender,
                number,
            )

            spacy_tokens.append(spacy_token)

        return spacy_tokens

    def get_source(self, parsed_object):
        is_contraction_part = parsed_object.text.endswith("'")
        is_inverted_subject_pron = parsed_object.text.startswith("-")
        is_verb = self.get_pos_string(parsed_object.pos_) == "verb"
        is_proper_noun = self.get_pos_string(parsed_object.pos_) == "proper noun"

        lemma_front = is_contraction_part or is_inverted_subject_pron or is_verb

        if lemma_front:
            front = parsed_object.lemma_
        else:
            front = parsed_object.text

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

    def get_openai_tokens(self, spacy_tokens):
        request_string = self.text.source

        request_tokens = []

        for spacy_token in spacy_tokens:
            request_token = {
                "representation": spacy_token.representation,
                "source": spacy_token.source,
                "pos": spacy_token.pos,
                "gender": spacy_token.gender,
                "number": spacy_token.number,
            }
            request_tokens.append(request_token)

        request = {
            "string": request_string,
            "tokens": request_tokens,
        }

        response_objects = self.session.openai.get_tokens(request)

        openai_tokens = []

        for response_object in response_objects:
            openai_token = OpenAiToken(response_object)
            openai_tokens.append(openai_token)

        return openai_tokens

    def create_tokens(self, spacy_tokens, openai_tokens):
        if len(spacy_tokens) != len(openai_tokens):
            raise Exception("spacy_tokens is not the same length as openai_tokens")

        # Add details from both tokens to token and add to self

        return self
