from models.session import Session
from models.source import Source


class UserInterface:
    def __init__(self, session):
        self.session = session

    def choose_deck(self):
        deck_dict = self.session.anki_interface.get_decks()

        print("\nChoose a deck:")
        for i, (deck_name, deck_id) in enumerate(deck_dict.items(), 1):
            print(f"{i}. {deck_name} (ID: {deck_id})")

        while True:
            user_input = input("\nEnter the number of the deck you want to work in: ")

            try:
                choice = int(user_input)
            except:
                print("\nPlease enter a valid number.")
                continue

            try:
                deck_id = deck_dict[deck_name]
                deck_name = list(deck_dict.keys())[choice - 1]
                self.session.anki_interface.deck_id = deck_id
                self.session.anki_interface.deck_name = deck_name
                print(f"\nDeck selected: {deck_name} (ID: {deck_id})")
                break
            except:
                print("\nInvalid choice. Please select a number from the list.")
                continue

    def request_input(self):
        while True:
            user_input = input(
                "\nEnter a string in French (or type 'exit' to quit):\n\n"
            )

            if user_input == "exit":
                break

            translation = Source(self.session, user_input)
