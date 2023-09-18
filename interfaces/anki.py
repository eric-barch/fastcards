import json
import urllib.request


class AnkiInterface:
    def __init__(self, session):
        self.session = session
        session.anki_interface = self
        self.read_deck_name = None
        self.write_deck_name = None

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

    def find_notes_by_front(self, front):
        query = f'deck:"{self.read_deck_name}" "front:{front}"'

        return self.call_api(
            "findNotes",
            query=query,
        )

    def add_note(self, front_content, back_content):
        return self.call_api(
            "addNote",
            note={
                "deckName": "Français::Harry Potter à l'école des sorciers",
                "modelName": "Basic",
                "fields": {"Front": front_content, "Back": back_content},
                "options": {"allowDuplicate": False},
                "tags": [],
            },
        )
