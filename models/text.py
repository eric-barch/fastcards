import spacy

from models.token import Token

nlp = spacy.load("fr_dep_news_trf")


class Text:
    def __init__(self, input):
        super().__init__()
        self.string = input
        self.tokens = self.tokenize(input)

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

    def get_marked_string(self):
        marked_text = self.string
        offset = 0

        for token in self.tokens:
            if token.marked_for_lookup:
                start = token.start + offset
                end = token.end + offset
                marked_text = (
                    marked_text[:start]
                    + "["
                    + marked_text[start:end]
                    + "]"
                    + marked_text[end:]
                )
                offset += 2  # account for the added brackets

        print(marked_text)

        return marked_text

    def get_marked_tokens(self):
        marked_tokens = []

        for token in self.tokens:
            if token.marked_for_lookup:
                marked_tokens.append(token)

        return marked_tokens

    def __str__(self):
        return "\n".join(str(token) for token in self.tokens)