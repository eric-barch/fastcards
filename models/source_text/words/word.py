class Word:
    def __init__(self, words, word, word_index):
        self.session = words.session
        self.french = word
        self.word_index = word_index
        self.english = self.session.openai_interface.get_english_translation(
            self.french
        )
        print(self)

    def __repr__(self):
        return f"{self.french} ({self.english})"
