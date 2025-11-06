import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import requests
import sys

if not nltk.download('punkt', quiet=True):
    nltk.download('punkt')
if not nltk.download('wordnet', quiet=True):
    nltk.download('wordnet')

class Word():
    def __init__(self, user_word):
        if not isinstance(user_word, str):
            raise ValueError("Must be a string/text")
        elif len(user_word) <= 2:
            raise ValueError("Must be an English word with more than 2 letters")
        else:
            synsets = wn.synsets(user_word)
            if len(synsets) > 0:
                self._user_word = user_word
            else:
                raise ValueError("Invalid English word")

    def __str__(self):
        return self._user_word

    @classmethod
    def get(cls):
        while True:
            user_word = str(input("Quote with exact word included: ")).strip().lower()
            try:
                return Word(user_word)
            except ValueError as e:
                print(e)

def main():
    word = str(Word.get())
    q_data = request_data()
    quote_list = filter_data(q_data, word)
    saying = quote_filter(quote_list, word)
    print(saying)

def request_data():
#Inspirational quotes provided by "https://zenquotes.io/"
    try:
        response = requests.get("https://zenquotes.io/api/quotes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        sys.exit(e)

def filter_data(q_data, word):
    q_list = []

    try:
        for item in q_data:
            quote = item["q"]
            author = item["a"]
            if word in quote:
                q_list.append((quote, author))
        return q_list
    except KeyError as e:
        sys.exit(e)

def quote_filter(quote_list, word):
    try:
        for saying in quote_list:
            tokens = word_tokenize(saying[0])
            if word in tokens:
                return saying
        else:
            return str("Try again; no quote found matching the exact Word/Mood")
    except IndexError as e:
        sys.exit(e)

if __name__ == "__main__":
    main()
