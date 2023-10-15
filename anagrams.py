import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
import itertools
stop_words = set(stopwords.words('english'))
# print(stop_words)
wordsList = ["two", "ducks"]
tagged = nltk.pos_tag(wordsList)
celeb_name = "Sophie Daguin"
a = itertools.permutations(celeb_name, len(celeb_name)-1)
for b in a:
    mix = "".join(b)
    split = mix.split(" ")
    for i in split:
        if i in words.words():
            print(i)