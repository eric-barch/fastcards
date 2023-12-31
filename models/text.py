import spacy

from models.token import Token

nlp = spacy.load("fr_dep_news_trf")


class Text:
    def __init__(self, input):
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
        marked_string = self.string
        offset = 0

        for token in self.tokens:
            if token.will_look_up:
                start = token.start + offset
                end = token.end + offset
                marked_string = (
                    marked_string[:start]
                    + "["
                    + marked_string[start:end]
                    + "]"
                    + marked_string[end:]
                )
                offset += 2

        return marked_string

    def get_marked_tokens(self):
        marked_tokens = []

        for token in self.tokens:
            if token.will_look_up:
                marked_tokens.append(token)

        return marked_tokens

    def get_new_notes(self):
        new_notes = []

        for token in self.tokens:
            for note in token.get_notes():
                if not note.id:
                    new_notes.append(note)

        return new_notes
