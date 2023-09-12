import json
import os

import openai
from dotenv import load_dotenv


class OpenAiInterface:
    def __init__(self, session):
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

    def get_french_and_english_system_prompt(self):
        return """
          You will receive a string in French. There may be misspellings or improper/missing 
          accentation. You should return a JSON object with the fields "french" and "english".
          The "french" field should contain a cleaned up version of the input string (correct
          any misspellings, add any accents, etc.) in French. The "english" field should contain 
          the English translation of the input string. For both fields, use the context of the 
          entire string to determine the intended meaning.

          Example Input/Output:

          Input: Ils continuerent leurs emplettes dans les boutiques qui s'alignaient le long de la rue et bientot
          Output: {
            "french": "Ils continuèrent leurs emplettes dans les boutiques qui s'alignaient le long de la rue et bientôt",
            "english": "They continued their shopping in the shops that lined the street and soon"
          }

          Input: Vous netes pas oblige, dit-il. Je le sais bien, mais je veux t'offrir un animal.
          Output: {
            "french": "Vous n'êtes pas obligé, dit-il. Je le sais bien, mais je veux t'offrir un animal.",
            "english": "You are not obliged, he said. I know, but I want to give you an animal."
          }

          Input: Il y avait des tas de choses a acheter: des robes, des gants, des chapeaux, des bottes
          Output: {
            "french": "Il y avait des tas de choses à acheter: des robes, des gants, des chapeaux, des bottes",
            "english": "There were lots of things to buy: dresses, gloves, hats, boots"
          }
        """

    def get_french_and_english(self, input):
        system_prompt = self.get_french_and_english_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj

    def deconstruct_french_system_prompt(self):
        return """
          You will receive a string in French. Return a JSON array containing the string's
          constituent words. Adhere to the following rules:

          1.  Deconstruct any contractions into their constituent words. 
              Example: m'appelle -> me appeler
          2.  Make verbs infinitive. Use the context of the entire string to confirm
              that the input word is indeed a conjugated verb and not some other part of speech.
              Example: appelle -> appeler
          3.  Make nouns singular.
              Example: cadeaux -> cadeau
          4.  Make adjectives masculine.
              Example: mauvaise -> mauvais
          
          Below you will find some examples of input and output. Model your response after these
          examples.

          Input: Bonjour, je m'appelle Harry Potter. Je suis un sorcier.
          Output: ["bonjour", "je", "me", "appeler", "Harry", "Potter", "je", "être", "un", "sorcier"]

          Input: Au-dessus de la porte, des lettres d'or écaillées indiquaient : << Ollivander >>
          Output: ["au-dessus", "de", "le", "porte", "des", "lettre", "de", "or", "écailler", "indiquer", "Ollivander"]

          Input: Ce ne serait pas une mauvaise idee, repondit Hagrid. De toute facon, tu n'en sais pas encore assez pour jeter des sorts.
          Output: ["ce", "ne", "être", "pas", "une", "mauvais", "idée", "répondre", "Hagrid", "de", "tout", "façon", "tu", "ne", "en", "savoir", "pas", "encore", "assez", "pour", "jeter", "des", "sort"]
        """

    def deconstruct_french(self, french_string):
        system_prompt = self.deconstruct_french_system_prompt()
        response_str = self.call_api(system_prompt, french_string)
        response_obj = json.loads(response_str)
        return response_obj

    def get_word_details_system_prompt(self):
        return """
          You will receive a JSON object in the following format:

          {
            "string": "string",
            "words": [
              "word1",
              "word2",
              "word3",
              ...
            ],
            "word_index": integer,
            "word": "word"
          }

          The "string" field contains the original string in French. The "words" field contains the
          constituent words of the "string" field in order, sometimes with minor changes made to
          that word's form to standardize tense, masculinity, etc. The "word_index" field contains 
          the index of the word in the "words" field that you should return details for. The "word"
          field contains the string value of the word at the index specified by the "word_index" field.
          This is provided so you can confirm that you are returning details for the correct word.

          Return a JSON object containing the following fields for the specified word:

          {
            "word": the original word from the "word" field in French,
            "english": the English translation of the word,
            "part_of_speech": the part of speech of the word,
            "french_definition": the definition of the word in French,
            "english_definition": the definition of the word in English
          }

          For part of speech, choose the best fit from the following list:
            - noun
            - verb
            - adjective
            - adverb
            - pronoun
            - preposition
            - conjunction
            - interjection
            - article
        """

    def get_word_details(self, string, words, word_index, word):
        system_prompt = self.get_word_details_system_prompt()
        user_string = f'{{"string": "{string}", "words": {json.dumps(words)}, "word_index": {word_index}, "word": "{word}"}}'

        # print(f"User string: {user_string}")
        # print(f"User string type: {type(user_string)}")

        response_str = self.call_api(
            system_prompt,
            user_string,
        )
        response_obj = json.loads(response_str)

        return response_obj
