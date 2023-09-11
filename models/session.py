class Session:
    def __init__(self):
        self.user_interface = None
        self.anki_interface = None
        self.openai_interface = None
        self.translation = None

    def __repr__(self):
        raise Exception("session.__repr__() not implemented.")
