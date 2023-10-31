import spacy

from global_vars import column_widths
from models.token import Token

nlp = spacy.load("fr_dep_news_trf")


class Tokens(list):
    def __init__(self, input):
        super().__init__()
        self.extend(self.tokenize(input))

    def tokenize(self, input):
        nlp_tokens = nlp(input)

        tokens = []

        for nlp_token in nlp_tokens:
            if nlp_token.pos_ == "PUNCT":
                continue

            token = Token(
                nlp_token.text,
                nlp_token.lemma_,
                nlp_token.pos_,
                nlp_token.idx,
                nlp_token.idx + len(nlp_token.text),
            )

            tokens.append(token)

        return tokens

    def __str__(self):
        header = (
            f"{'token':<{column_widths[0]}}"
            f"{'existing_note_source':<{column_widths[1]}}"
            f"{'existing_note_target':<{column_widths[2]}}"
            f"{'lemma':<{column_widths[3]}}"
            f"{'existing_note_source':<{column_widths[4]}}"
            f"{'existing_note_target':<{column_widths[5]}}"
            f"{'pos':<{column_widths[6]}}"
        )
        tokens = "\n".join(str(token) for token in self)
        return f"{header}\n{tokens}"
