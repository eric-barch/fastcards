class Word:
    def __init__(self, words, word_index, word):
        self.session = words.session
        self.words = words
        self.word_index = word_index
        self.french = word
        self.english = None
        self.part_of_speech = None
        self.french_definition = None
        self.english_definition = None

    def __repr__(self):
        return f"{self.french}\n{self.english}\n{self.part_of_speech}\n{self.french_definition}\n{self.english_definition}"

    def populate(self):
        string = self.words.french
        words = [word.french for word in self.words]
        word_index = self.word_index
        word = self.french

        response = self.session.openai_interface.get_word_details(
            string, words, word_index, word
        )

        print(f"\nWord details: {response}")
