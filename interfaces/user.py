from models.source_string.source_string import SourceString


class UserInterface:
    def __init__(self, session):
        self.session = session

    def choose_deck(self):
        deck_names = self.session.anki_interface.get_deck_names()

        print("\nChoose a deck:")
        for i, deck_name in enumerate(deck_names, start=1):
            print(f"{i}. {deck_name}")

        while True:
            user_input = input("\nEnter the number of the deck to add cards to: ")

            try:
                choice = int(user_input)
            except:
                print("\nPlease enter a valid number.")
                continue

            try:
                deck_name = deck_names[choice - 1]
                self.session.anki_interface.deck_name = deck_name
                print(f"\nDeck selected: {deck_name}")
                break
            except:
                print("\nInvalid choice. Please select a number from the list.")
                continue

    def request_string(self):
        while True:
            user_input = input(
                "\nEnter a string in French (or type 'exit' to quit):\n\n"
            )

            if user_input == "exit":
                break

            SourceString(self.session, user_input)
