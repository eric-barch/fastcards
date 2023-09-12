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

    def get_french_and_english_strings_system_prompt(self):
        return """You will receive a string in French. There may be misspellings or 
          improper/missing accentation. You should return a JSON object with the fields "french" 
          and "english". The "french" field should contain a cleaned up version of the input string
          (correct any misspellings, add any accents, etc.) in French. The "english" field should 
          contain the English translation of the input string. For both fields, use the context of 
          the entire string to determine the intended meaning.

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
          }"""

    def get_french_and_english_strings(self, input):
        system_prompt = self.get_french_and_english_strings_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj

    def deconstruct_french_string_system_prompt(self):
        return """
          You will receive a string in French. Return a JSON array containing the string's
          constituent words. Adhere to the following rules:

          1.  Make verbs infinitive. Use the context of the entire string to confirm
              that the input word is indeed a conjugated verb. If a conjugated verb is being used
              as an adjective, adverb, or noun, do not make it infinitive.
              Examples:
              appelle -> appeler
              sais -> savoir
              suis -> être
              délabrée -> délabrée (stays the same because it is an adjective)
          2.  Deconstruct any contractions (usually, two words joined by an apostrophe) into their 
              constituent words. 
              Example: 
              m'appelle -> me appeler
              n'en -> ne en
              l'école -> le école
              j'allais -> je aller
              d'un -> de un
          
          Below you will find some examples of input and desired output.

          Input: Bonjour, je m'appelle Harry Potter. Je suis un sorcier.
          Output: ["bonjour", "je", "me", "appeler", "Harry", "Potter", "je", "être", "un", "sorcier"]

          Input: Au-dessus de la porte, des lettres d'or écaillées indiquaient : << Ollivander >>
          Output: ["au-dessus", "de", "la", "porte", "des", "lettres", "de", "or", "écailler", "indiquer", "Ollivander"]

          Input: Ce ne serait pas une mauvaise idée, répondit Hagrid. De toute façon, tu n'en sais pas encore assez pour jeter des sorts.
          Output: ["ce", "ne", "être", "pas", "une", "mauvaise", "idée", "répondre", "Hagrid", "de", "toute", "façon", "tu", "ne", "en", "savoir", "pas", "encore", "assez", "pour", "jeter", "des", "sorts"]

          Input: La dernière boutique dans laquelle ils pénétrèrent était étroite et délabrée.
          Output: ["la", "dernière", "boutique", "dans", "laquelle", "ils", "pénétrer", "être", "étroite", "et", "délabrée"]
        """

    def deconstruct_french_string(self, french_string):
        system_prompt = self.deconstruct_french_string_system_prompt()
        response_str = self.call_api(system_prompt, french_string)
        response_obj = json.loads(response_str)
        return response_obj

    def get_word_details_system_prompt(self):
        return """
          You will receive a single French word. Return a JSON object containing the word details
          as formatted below.

          {
            "english": word's English translation,
            "part_of_speech": word's part of speech,
            "gender": word's gender, or null if not applicable,
          }

          If the word is a verb, its English translation should usually be preceded by "to",
          e.g. "to be", "to have", "to go", etc.

          For part_of_speech, choose the best fit from the following list:
            - "noun"
            - "proper noun"
            - "verb"
            - "adjective"
            - "adverb"
            - "pronoun"
            - "preposition"
            - "conjunction"
            - "interjection"
            - "article"
          
          For gender, choose one of the following three options:
            - "masculine"
            - "feminine"
            - null (if the concept of gender does not apply to the word)
        """

    def get_word_details(self, word):
        system_prompt = self.get_word_details_system_prompt()
        user_string = word

        response_str = self.call_api(
            system_prompt,
            user_string,
        )
        response_obj = json.loads(response_str)

        return response_obj
