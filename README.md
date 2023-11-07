# fastcards

Make Anki language flashcards faster.

## Use Case

[Anki](https://apps.ankiweb.net/) is a free, open-source flashcard program. Its use of [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) makes it good for building and retaining a new vocabulary. But making flashcards is time-consuming and borderline distracting when you're trying to work through a text in a new language. You often end up creating cards only for "true" vocabulary terms like nouns, verbs, adjectives, etc., leaving you with a weak understanding of articles and other connectors. Fastcards accepts string input as you read, and automatically destructures the string, tells you which component terms you already know, and gives you the option to generate flashcards for new ones.

## Dependencies

- The [OpenAI API](https://platform.openai.com/docs/models) is used to translate and tag terms. You will need to supply your own OpenAI API key.
- spaCy's [natural language processing models](https://spacy.io/models) (in this example, [French](https://spacy.io/models/fr#fr_dep_news_trf)) are used to tokenize input. They are free and run locally.
- The [AnkiConnect](https://github.com/FooSoft/anki-connect) Anki plugin is used to interface with Anki's underlying database.

## Install and Setup

## How to Use

## Adapt for Other Languages
