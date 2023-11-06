# fastcards

Make Anki language flashcards faster.

## When to Use

A good way to start learning a new language is to immerse yourself in a text written in that language. Making flashcards ensures that new terms are added to your review pool as soon as they are encountered.

[Anki](https://apps.ankiweb.net/) is a free, open-source flashcard program. Its use of [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) makes it good for building and retaining a new vocabulary.

But making flashcards is time-consuming. Because of the friction, you often end up only creating cards for "true" vocabulary terms like nouns, verbs, adjectives, etc. Articles, connectors, and the like often get left out, and you end up with a weak understanding of those terms.

With fastcards, you simply type in a string in your source language, and it automatically destructures the string, tells you which terms you already have, and gives you the option to generate flashcards for new terms.

## Dependencies

- The OpenAI API (specifically [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)) is used to translate and tag terms. You will need to supply your own OpenAI API key.
- spaCy's [natural language processing models](https://spacy.io/models) (in this example, [French](https://spacy.io/models/fr#fr_dep_news_trf)) are used to tokenize input. They are free and run locally.

## Install and Setup

## How to Use

## Adapt for Other Languages
