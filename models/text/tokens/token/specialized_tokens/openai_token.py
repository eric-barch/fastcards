class OpenAiToken:
    def __init__(self, response_object):
        self.source = response_object["source"]
        self.target = response_object["target"]
        self.pos = response_object["pos"]
        self.gender = response_object["gender"]
        self.number = response_object["number"]
