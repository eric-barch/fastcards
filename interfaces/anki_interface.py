import json
import urllib.request
from models.note import Note


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

    def set_read_and_write_decks(self, read_deck, write_deck):
        self.read_deck = read_deck
        self.write_deck = write_deck

    def check_for_existing_notes(self, tokens):
        for token in tokens:
            self.find_notes(token.text)
            self.find_notes(token.lemma)

    def find_notes(self, potential_note):
        query = f'deck:"{self.read_deck}" source:"{potential_note.text}"'
        response = self.call_api("findNotes", query=query)
        if response:
            notes_info = self.call_api("notesInfo", notes=response)
            fields = notes_info[0].get("fields")
            potential_note.source = fields.get("source").get("value")
            potential_note.target = fields.get("target").get("value")
