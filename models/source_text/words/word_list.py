import json
from models.source_text.words.word_details import WordDetails


class WordList(list):
    def __init__(self, session, french_string):
        super().__init__()
        self.session = session
        self.french_string = french_string
        self.get_all_words()
        self.get_unique_words()
        self.get_noteless_words()
        self.create_word_objects()

    def get_all_words(self):
        self.all_words = self.session.openai_interface.deconstruct_french_string(
            self.french_string
        )
        print(f"all_words: {json.dumps(self.all_words)}")

    def get_unique_words(self):
        self.unique_words = []
        for word in self.all_words:
            if word not in self.unique_words:
                self.unique_words.append(word)
        print(f"unique_words: {json.dumps(self.unique_words)}")

    def get_noteless_words(self):
        self.noteless_words = []
        for word in self.unique_words:
            note_id = self.session.anki_interface.check_for_note(word)
            if note_id:
                print(f"Note already exists: {word} (ID: {note_id})")
            else:
                self.noteless_words.append(word)
        print(f"noteless_words: {json.dumps(self.noteless_words)}")

    def create_word_objects(self):
        for word in self.noteless_words:
            word_details = WordDetails(
                self.session,
                self,
                word,
            )
            self.append(word_details)

        # for response in responses:
        #     word_details = WordDetails(
        #         self.session,
        #         self,
        #         response["french"],
        #         response["english"],
        #         response["part_of_speech"],
        #         response["is_masculine"],
        #     )
        #     self.append(word_details)
