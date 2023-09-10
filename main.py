from apis.openai_interface import OpenAiInterface
from apis.anki_interface import AnkiInterface
from session import Session


def main():
    session = Session()

    anki_interface = AnkiInterface(session)
    openai_interface = OpenAiInterface(session)

    deck_dict = anki_interface.get_decks()
    decks = list(deck_dict.keys())

    print("\nPick a deck:")
    for idx, (deck_name, deck_id) in enumerate(deck_dict.items(), 1):
        print(f"{idx}. {deck_name} (ID: {deck_id})")

    while True:
        try:
            choice = int(input("\nEnter the number of your choice: "))
            if 1 <= choice <= len(decks):
                session.deck_name = decks[choice - 1]
                session.deck_id = deck_dict[decks[choice - 1]]
                print(f"\nDeck selected: {decks[choice-1]}")
                break
            else:
                print("\nInvalid choice. Please select a number from the list.")
        except ValueError:
            print("\nPlease enter a valid number.")

    while True:
        string = input("\nEnter a string in French (or type 'exit' to quit):\n\n")
        if string.lower() == "exit":
            break
        session.string = string
        response = openai_interface.deconstruct_string()
        print(response)


if __name__ == "__main__":
    main()
