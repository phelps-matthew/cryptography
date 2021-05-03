import nltk
from nltk.book import *

sentence = "Here is a test sentence that I wrote off the top of my head."

tokens = nltk.word_tokenize(sentence)
print(tokens)
