import openai
from dotenv import load_dotenv
import os


class OpenAiInterface:
    def __init__(self, session):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.session = session

    def call_api(self, string: str, systemPrompt: str):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": systemPrompt},
                {
                    "role": "user",
                    "content": f"Sentence: {string}",
                },
            ],
        )
        return response.choices[0].message.content

    def deconstruct_string_system_prompt(self):
        return """
          You will receive a string in French. Please do the following to it:

          1. Translate the entire string to English.
          2. Deconstruct the french string into its constituent words in lowercase except for proper nouns.
              e.g. "Bonjour, je m'appelle Harry Potter." -> [bonjour, je, m'appelle, Harry, Potter]
          3. Deconstruct any contractions into their constituent words.
              e.g. [bonjour, je, m'appelle, Harry, Potter] -> [bonjour, je, me, appelle, Harry, Potter]
          4. Convert any verbs to their infinitive form.
              e.g. [bonjour, je, me, appelle, Harry, Potter] -> [bonjour, je, me, appeler, Harry, Potter]
          5. Add any accents that were missing in the input.
              e.g. "ecole" -> "école"
          
          Your response should be a JSON object with the following fields:

          {
              "englishSentence": from step 1,
              "words": // an array of strings from step 5.
          }

          If for some reason you cannot complete the request, return the following:
          
          {"error": "error message"}
          
          You should generally be able to determine when to throw this error. Here are some
          concrete examples of times you should definitely return the error:
          - You receive some input that is not a French string.
          - The input is too long for you to process.
        """

    def deconstruct_string(self):
        systemPrompt = self.deconstruct_string_system_prompt()
        response = self.call_api(self.session.string, systemPrompt)
        self.session.deconstructed_words = response
        return response
