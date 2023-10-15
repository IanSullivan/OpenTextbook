from haystack.document_stores import FAISSDocumentStore, InMemoryDocumentStore
from haystack.nodes import FARMReader, QuestionGenerator
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import EmbeddingRetriever, DensePassageRetriever
from haystack.nodes import Seq2SeqGenerator
from haystack.utils import print_answers, print_documents
from haystack.nodes import FARMReader, QuestionGenerator
from haystack.pipelines import QuestionAnswerGenerationPipeline, SearchSummarizationPipeline, QuestionGenerationPipeline
from haystack.pipelines import GenerativeQAPipeline
from haystack import Pipeline
from haystack.nodes import DocumentMerger

from transformers import pipeline
import re
from haystack.utils import print_questions
from haystack.nodes import TransformersSummarizer
# document_store = FAISSDocumentStore(embedding_dim=128, faiss_index_factory_str="Flat", sql_url="sqlite:///philosophy.db")

document_store = FAISSDocumentStore.load("data/philosophy.faiss")
retriever = EmbeddingRetriever(document_store=document_store,
                               embedding_model="yjernite/retribert-base-uncased",
                               model_format="retribert",
                               use_gpu=True)
generator = Seq2SeqGenerator(model_name_or_path="vblagoje/bart_lfqa", use_gpu=False)
# pszemraj/t5-base-askscience-lfqa
pipe = GenerativeQAPipeline(generator, retriever)
import time
time1 = time.time()
for i in range(2):
    a = pipe.run(
        query="Who was Plato?", params={"Retriever": {"top_k": 5}}

    )
    print(a)
print(abs(time.time() - time1))
# summarizer = pipeline("summarization", "sshleifer/distilbart-cnn-12-6")
# reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
# reader = FARMReader(model_name_or_path="distilbert-base-uncased-distilled-squad")
# reader = FARMReader(model_name_or_path="huawei-noah/TinyBERT_General_6L_768D", use_gpu=True)
# question_generator = QuestionGenerator(model_name_or_path="mrm8488/t5-base-finetuned-question-generation-ap", use_gpu=False)
# summarizer = TransformersSummarizer(model_name_or_path="google/pegasus-xsum", use_gpu=False, max_length=10000)
# summarizer = TransformersSummarizer(model_name_or_path="sshleifer/distilbart-cnn-12-6", use_gpu=False, min_length=200, max_length=1000)
# document_merger = DocumentMerger(separator=" ")

# pipeline = Pipeline()
# #
# pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
# pipeline.add_node(component=document_merger, name="Document Merger", inputs=["Retriever"])
# pipeline.add_node(component=summarizer, name="Summarizer", inputs=["Document Merger"])

# result = pipeline.run(query="Who was Plato", params={"Retriever": {"top_k": 5, "headers": None}})
# print(result)
# pipe = SearchSummarizationPipeline(retriever=retriever, summarizer=summarizer)
# result = pipeline.run(query="Describe Luna Lovegood.", params={"Retriever": {"top_k": 5}})
# pipe = ExtractiveQAPipeline(reader, retriever)
#
# querying_pipeline = Pipeline()
# querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
# querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])
# question_generation_pipeline = QuestionGenerationPipeline(question_generator)
# qag_pipeline = QuestionAnswerGenerationPipeline(question_generator, reader=reader)
# print("ham")
# prediction = pipe.run(
#     query="What doth life?",
#     params={
#         "Retriever": {"top_k": 10},
#         "Reader": {"top_k": 5}
#     }
# )
# print(type(prediction['answers'][0]))
# print(prediction['answers'][0].to_dict().keys())
# print(prediction['answers'][0].to_dict()['answer'])
# print(prediction['answers'][0].to_dict()['score'])
# print()
# print(prediction['answers'][1].to_dict()['answer'])
# print(prediction['answers'][1].to_dict()['score'])

# print_answers(prediction)

# for idx, document in enumerate(document_store):
#
#     print(f"\n * Generating questions and answers for document {idx}: {document.content[:50]}...\n")
#     result = qag_pipeline.run(documents=[document], params={"Reader": {"top_k": 5}})
#     # result = question_generation_pipeline.run(documents=[document])
#     print_questions(result)