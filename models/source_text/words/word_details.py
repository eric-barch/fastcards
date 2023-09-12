import json


class WordDetails:
    def __init__(
        self, session, word_list, french, english, part_of_speech, is_masculine
    ):
        self.session = session
        self.word_list = word_list
        self.french = french
        self.english = english
        self.part_of_speech = part_of_speech
        self.is_masculine = is_masculine
        print(f"{self}")

    def __repr__(self):
        return json.dumps(
            {
                "french": self.french,
                "english": self.english,
                "part_of_speech": self.part_of_speech,
                "is_masculine": self.is_masculine,
            },
            indent=2,
        )
