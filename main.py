from models.session import Session


def main():
    session = Session()

    session.user_interface.choose_decks()
    session.user_interface.request_string()


if __name__ == "__main__":
    main()
