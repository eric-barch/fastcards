class Session:
    def __init__(self):
        self.deck_name = None
        self.deck_id = None
        self.string = None
        self.deconstructed_words = []

    # Representation of the object for better visualization
    def __repr__(self):
        return f"""
          Session:
          deck_name={self.deck_name},
          deck_id={self.deck_id}, 
          sentence='{self.string}', 
          deconstructed_words={self.deconstructed_words}
        """
