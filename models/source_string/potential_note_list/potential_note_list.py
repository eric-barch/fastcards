import json
import spacy

nlp = spacy.load("fr_core_news_sm")


class PotentialNoteList(list):
    def __init__(self, session, string):
        super().__init__()
        self.session = session
        self.string = string

        parsed_tokens = self.parse_tokens()

        request_tokens = self.get_request_tokens(parsed_tokens)
        request = json.dumps(
            {
                "string": self.string,
                "tokens": request_tokens,
            },
            indent=4,
        )

        translated_tokens = self.session.openai_interface.translate_tokens(request)

        self.tokens = self.set_tokens(parsed_tokens, translated_tokens)
        print(f"\ntokens: {json.dumps(self.tokens, indent=4)}")

    def parse_tokens(self):
        parsed_string = nlp(self.string)

        parsed_tokens = []

        for token in parsed_string:
            if token.pos_ != "PUNCT":
                note_front = self.get_note_front(token)

                morph = token.morph.to_dict()

                gender_abbr = morph.get("Gender")
                gender = self.get_gender_string(gender_abbr) if gender_abbr else None

                number_abbr = morph.get("Number")
                number = self.get_number_string(number_abbr) if number_abbr else None

                parsed_token = {
                    "note_front": note_front,
                    "representation": token.text,
                    "start": token.idx,
                    "end": token.idx + len(token.text),
                    "lemma": token.lemma_,
                    "pos": self.get_pos_string(token.pos_),
                    "gender": gender,
                    "number": number,
                }

                parsed_tokens.append(parsed_token)

        return parsed_tokens

    def get_note_front(self, token):
        is_contraction_part = token.text.endswith("'")
        is_inverted_subject_pron = token.text.startswith("-")
        is_verb = self.get_pos_string(token.pos_) == "verb"

        lemma_front = is_contraction_part or is_inverted_subject_pron or is_verb

        if lemma_front:
            return token.lemma_

        return token.text

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
                "note_front": token["note_front"],
                "pos": token["pos"],
            }
            request_tokens.append(request_token)

        return request_tokens

    def set_tokens(self, parsed_tokens, translated_tokens):
        if len(parsed_tokens) != len(translated_tokens):
            raise Exception(
                "parsed_tokens and translated_tokens must be the same length"
            )

        tokens = parsed_tokens

        for i, token in enumerate(tokens):
            translated_token = translated_tokens[i]

            if token["note_front"] != translated_token["note_front"]:
                token["note_front"] = translated_token["note_front"]
                token["pos"] = "verb"

            token["english"] = translated_token["english"]

        self.tokens = tokens
        return self.tokens
