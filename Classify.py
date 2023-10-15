from transformers import DistilBertTokenizer, DistilBertModel
import torch
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

import transformers
import torch
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
from transformers import BertTokenizer, BertModel, BertConfig

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased', return_dict=True)
for i, param in enumerate(model.base_model.parameters()):
    if i < 95:
        param.requires_grad = False

for i in range(200):
    inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
    print(inputs)
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state
print(outputs.last_hidden_state)


class BERTClass(torch.nn.Module):
    def __init__(self):
        super(BERTClass, self).__init__()
        self.l1 = transformers.BertModel.from_pretrained('bert-base-uncased')
        self.l2 = torch.nn.Dropout(0.3)
        self.l3 = torch.nn.Linear(768, 6)

    def forward(self, ids, mask, token_type_ids):
        _, output_1 = self.l1(ids, attention_mask=mask, token_type_ids=token_type_ids)
        output_2 = self.l2(output_1)
        output = self.l3(output_2)
        return output