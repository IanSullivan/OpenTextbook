from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

sentence = ['This framework generates embeddings for each input sentence']
sentence2 = ['With this framework we may be able to generate embedding for an input sentence']
sentence3 = ['With this framework we cannot generate embedding for an input sentence']


#Sentences are encoded by calling model.encode()
A = model.encode(sentence)[0]
B = model.encode(sentence2)[0]
cosine = np.dot(A, B)/(norm(A)*norm(B))
print(cosine)
B = model.encode(sentence3)[0]
cosine = np.dot(A, B)/(norm(A)*norm(B))
print(cosine)