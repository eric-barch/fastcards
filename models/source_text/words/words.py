from models.source_text.words.word import Word


class Words(list):
    def __init__(self, source_text):
        super().__init__()
        self.session = source_text.session
        self.french = source_text.french
        self.init_word_objects()
        self.populate_word_objects()

    def init_word_objects(self):
        words = self.session.openai_interface.deconstruct_french(self.french)
        print(f"\nDeconstructed words: {words}")

        for word_index, word in enumerate(words):
            self.append(Word(self, word_index, word))

    def populate_word_objects(self):
        for word in self:
            word.populate()
