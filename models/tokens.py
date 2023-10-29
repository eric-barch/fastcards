import spacy

from .token import Token
from .spacy_token import SpacyToken
from .openai_token import OpenAiToken

nlp = spacy.load("fr_dep_news_trf")


class Tokens(list):
    def __init__(self, session, text):
        super().__init__()
        self.session = session
        self.text = text

        spacy_tokens = self.get_spacy_tokens()

        print()
        for spacy_token in spacy_tokens:
            print(
                f"{spacy_token.representation:<{15}}{spacy_token.lemma:<{15}}{spacy_token.start:<{10}}{spacy_token.end:<{10}}"
            )

        # openai_tokens = self.get_openai_tokens(spacy_tokens)

        # self.create_tokens(spacy_tokens, openai_tokens)

    def __repr__(self):
        indent = 5
        column_width = 20

        row_labels = ["representation", "source", "target", "pos", "gender", "number"]

        header_line = f"\n{'':<{indent}}{'':<{column_width}}{'spacy':<{column_width}}{'openai':<{column_width}}{'merged'}"

        repr_str = header_line

        for i, token in enumerate(self):
            token_repr = token.__repr__(
                number=i + 1,
                indent=indent,
                column_width=column_width,
                row_labels=row_labels,
            )
            repr_str += "\n\n" + token_repr

        return repr_str

    def get_spacy_tokens(self):
        source = self.text.source

        parsed_objects = nlp(source)

        spacy_tokens = []

        for parsed_object in parsed_objects:
            if parsed_object.pos_ == "PUNCT":
                continue

            spacy_token = SpacyToken(
                parsed_object.text,
                parsed_object.lemma_,
                parsed_object.idx,
                parsed_object.idx + len(parsed_object.text),
            )

            spacy_tokens.append(spacy_token)

        return spacy_tokens

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

        for i, spacy_token in enumerate(spacy_tokens):
            token = Token(self.text, spacy_token, openai_tokens[i])
            self.append(token)

        return self
