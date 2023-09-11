import json
import os

import openai
from dotenv import load_dotenv

from models.session import Session


class OpenAiInterface:
    def __init__(self, session: Session):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.session = session
        session.openai_interface = self

    def call_api(self, systemPrompt: str, string: str):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": systemPrompt},
                {
                    "role": "user",
                    "content": string,
                },
            ],
        )
        return response.choices[0].message.content

    def deconstruct_french_system_prompt(self):
        return """
          You will receive a string in French. Return a JSON array containing the string's
          constituent words. Adhere to the following rules:

          1. Convert any verb to its infinitive form. Use the context of the entire string to confirm
             that the word is indeed a conjugated verb and not some other part of speech.
             Example: "suis" -> "être"
          2. Deconstruct any contractions into their constituent words. 
             Example: "m'appelle" -> "me appeler"
          3. Make sure the arrays of words are properly accented for French. The user may not 
             properly accent the words in the input string. Use the context of the entire string
             to determine where accents should go.
             Example: "ecole" -> "école"
          
          Below you will find some examples of input and output. Model your response after these
          examples.

          Input: "Bonjour, je m'appelle Harry Potter. Je suis un sorcier."
          Output: ["bonjour", "je", "me", "appeler", "Harry", "Potter", "je", "être", "un", "sorcier"]

          Input: "Harry Potter a l'ecole des sorciers."
          Output: ["Harry", "Potter", "a", "le", "école", "des", "sorciers"]

          Input: "Ce ne serait pas une mauvaise idee, repondit Hagrid. De toute facon, tu n'en sais pas encore assez pour jeter des sorts."
          Output: ["ce", "ne", "être", "pas", "une", "mauvaise", "idée", "répondit", "Hagrid", "de", "toute", "façon", "tu", "ne", "en", "savoir", "pas", "encore", "assez", "pour", "jeter", "des", "sorts"]
        """

    def deconstruct_french(self, french_string):
        system_prompt = self.deconstruct_french_system_prompt()
        response_str = self.call_api(system_prompt, french_string)
        response_obj = json.loads(response_str)
        return response_obj

    def get_clean_french_system_prompt(self):
        return """
          You will receive a string in French. The user may not have properly accened and/or spelled
          the words in that string. Your job is to clean up the string (add any accents, correct
          any misspellings, etc.) using the context of the entire sentence to determine intended
          meaning.

          Example Input/Output:

          Input: ecole
          Output: école

          Input: Ils continuerent leurs emplettes dans les boutiques qui s'alignaient le long de la rue et bientot
          Output: Ils continuèrent leurs emplettes dans les boutiques qui s'alignaient le long de la rue et bientôt

          Input: Vous netes pas oblige, dit-il. Je le sais bien, mais je veux t'offrir un animal.
          Output: Vous n'êtes pas obligé, dit-il. Je le sais bien, mais je veux t'offrir un animal.
        """

    def get_clean_french(self, input):
        system_prompt = self.get_clean_french_system_prompt()
        response = self.call_api(system_prompt, input)
        return response

    def get_english_translation_system_prompt(self):
        return """
          You will receive a string in French. Return the English translation of that string.

          Example Input/Output:

          Input: Salut comment vas-tu?
          Output: Hi, how are you doing?

          Input: Je dois aussi t'offrir un cadeau pour ton anniversaire.
          Output: I also need to give you a gift for your birthday.

          Input: Vingt minutes plus tard, Harry sortit du magasin de chouettes avec une grande cage.
          Output: Twenty minutes later Harry came out of the owl shop with a large cage.
        """

    def get_english_translation(self, input):
        system_prompt = self.get_english_translation_system_prompt()
        response = self.call_api(system_prompt, input)
        return response
