from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForCausalLM, AutoModelForMaskedLM, AutoModelForSeq2SeqLM
from transformers import pipeline
import re
summarizer = pipeline("summarization", "sshleifer/distilbart-cnn-12-6")

ARTICLE = """ 
The principle of indifference, also known as the principle of insufficient reason, is attributed to Jacob Bernoulli, 
and sometimes to Laplace. Simply stated, it suggests that if there are n possible outcomes and there is no reason to 
view one as more likely than another, then each should be assigned a probability of 1/n. Quite appropriate for games of 
chance, in which dice are rolled or cards shuffled, the principle has also been referred to as the “classical” approach 
to probability assignments.
However, this principle has to be used with great care. Early examples include the event “two consecutive tosses of a 
coin will come up head.” If we know nothing about the coin, one may try to apply the principle and conclude that this 
event has probability 50%, but then the same argument would apply to any two outcomes of the two tosses. However, 
this type of counterexample can be ruled out by referring to the structure of the problem and arguing that there is 
sufficient reason to find three outcomes more likely than one.
More serious problems arise when we apply the principle to everyday problems, which are often not endowed with sufficient 
symmetries. For instance, assume that I ask you what is the probability that it will rain tomorrow.
"""


model = AutoModelForMaskedLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# txt = ""
# with open('data/textbooks/Philosophy/1 _What_is_Philosophy.txt') as f:
#     txt = f.read()
#
#     paragraphs = txt.split('\n\n')
#     for paragraph in paragraphs:
#         inputs = tokenizer.encode("summarize: " + paragraph, return_tensors="pt", truncation=True)
#         outputs = model.generate(inputs, max_length=1000, min_length=40, length_penalty=2.0, num_beams=4,
#                                  early_stopping=True)
#         print(tokenizer.decode(outputs[0][2:-1]))

# T5 uses a max_length of 512 so we cut the article to 512 tokens.
# print(txt)
# inputs = tokenizer.encode("summarize: " + txt, return_tensors="pt", truncation=True)
# outputs = model.generate(inputs, max_length=1000, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
# print(tokenizer.decode(outputs[0][1:]))

classifier = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
print(classifier(ARTICLE))