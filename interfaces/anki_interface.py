import json
import urllib.request


class AnkiInterface:
    def __init__(self, read_deck_name, write_deck_name):
        self.read_deck_name = read_deck_name
        self.write_deck_name = write_deck_name

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

    def get_all_deck_names(self):
        return self.call_api("deckNames")

    def find_notes(self, source):
        query = f'deck:"{self.read_deck_name}" source:"{source}"'
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
                    "deckName": self.write_deck_name,
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
