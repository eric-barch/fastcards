import json
import urllib.request


class AnkiInterface:
    def __init__(self):
        self.read_deck = None
        self.write_deck = None

    def call_api(self, action, **params):
        request = {"action": action, "params": params, "version": 6}
        requestJson = json.dumps(request).encode("utf-8")
        response = json.load(
            urllib.request.urlopen(
                urllib.request.Request("http://localhost:8765", requestJson)
            )
        )
        if len(response) != 2:
            raise Exception("Response has an unexpected number of fields.")
        if "error" not in response:
            raise Exception("Response is missing required error field.")
        if "result" not in response:
            raise Exception("Response is missing required result field.")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def get_all_decks(self):
        return self.call_api("deckNames")

    def set_decks(self, read_deck, write_deck):
        self.read_deck = read_deck
        self.write_deck = write_deck

    def check_for_existing(self, tokens):
        for token in tokens:
            existing_representations = self.find_notes(token.representation)
            existing_lemmas = self.find_notes(token.lemma)
            print(f"{token.representation} {existing_representations}")
            print(f"{token.lemma} {existing_lemmas}")

    def find_notes(self, front):
        query = f'deck:"{self.read_deck}" source:"{front}"'
        response = self.call_api("findNotes", query=query)
        return response

    def add_note(self, note):
        try:
            if note.pos_target == "proper noun":
                print(f"Skipped {note.source} (proper noun)")
                return

            return self.call_api(
                "addNote",
                note={
                    "deckName": self.write_deck,
                    "modelName": "Forward and Reverse with Grammatical Detail (Type Answer)",
                    "fields": {
                        "source": note.source,
                        "target": note.target,
                        "pos_source": note.pos_source,
                        "pos_target": note.pos_target,
                        "gender_source": note.gender_source,
                        "gender_target": note.gender_target,
                        "number_source": note.number_source,
                        "number_target": note.number_target,
                    },
                    "options": {"allowDuplicate": False},
                    "tags": [],
                },
            )
        except Exception as e:
            print(f"Skipped {note.source} ({e})")
