from models.source_text.words.word import Word


class Words(list):
    def __init__(self, source_text):
        super().__init__()
        self.session = source_text.session
        self.source_text = source_text
        self.create_words()

    def create_words(self):
        words = self.session.openai_interface.deconstruct_french(
            self.source_text.french
        )

        for word_index, word in enumerate(words):
            self.append(Word(self, word, word_index))
