import os
import re
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.schema import Document
from haystack import Pipeline
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import TextConverter, PreProcessor
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
from haystack.nodes import FARMReader, TransformersSummarizer, EmbeddingRetriever, Seq2SeqGenerator

from haystack.pipelines import ExtractiveQAPipeline, SearchSummarizationPipeline, GenerativeQAPipeline
import requests as req
from github import Github
import OpenAi
import json


class Agent:

    def __init__(self, agent_subject: str, init_db=False, fetch_github=False, use_gpu=True):
        self.agent_subject = agent_subject
        self.doc_dir = os.path.abspath(os.path.join("data/textbooks/", agent_subject))
        self.data_base_locations = "sqlite:///databases/{}/{}.db".format(agent_subject, agent_subject)
        self.doc_store_path = os.path.abspath(os.path.join("databases", agent_subject, "{}.faiss".format(agent_subject)))
        self.preprocessor = PreProcessor(clean_empty_lines=True,  clean_whitespace=True, clean_header_footer=False,
                                         split_by="word", split_length=100, split_respect_sentence_boundary=True)
        self.summaries = []
        self.document_store = None

        if fetch_github:
            self.fetch_github_documents()

        if init_db:
            self.initialize_document_store(128)
            self.retriever = EmbeddingRetriever(document_store=self.document_store, embedding_model="yjernite/retribert-base-uncased",
                                                model_format="retribert", use_gpu=False)
            self.document_store.update_embeddings(retriever=self.retriever)
            self.document_store.save(self.doc_store_path)
        else:
            self.document_store = FAISSDocumentStore.load(self.doc_store_path)
            self.retriever = EmbeddingRetriever(document_store=self.document_store,
                                                embedding_model="yjernite/retribert-base-uncased",
                                                model_format="retribert", use_gpu=False)

        self.reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
        self.summarizer = TransformersSummarizer(model_name_or_path="sshleifer/distilbart-cnn-12-6", use_gpu=False,
        # self.summarizer = TransformersSummarizer(model_name_or_path="t5-small", use_gpu=False,
                                                 min_length=50, max_length=500)
        self.generator = Seq2SeqGenerator(model_name_or_path="vblagoje/bart_lfqa", use_gpu=False)

        self.question_answering_pipe = ExtractiveQAPipeline(self.reader, self.retriever)
        self.search_summarizer_pipe = SearchSummarizationPipeline(summarizer=self.summarizer, retriever=self.retriever,
                                                                  generate_single_summary=True)
        self.long_form_answering_pipe = GenerativeQAPipeline(self.generator, self.retriever)

    def initialize_document_store(self, embedding_dim=128):
        for file in os.listdir(os.path.dirname(self.doc_store_path)):
            os.remove(os.path.join(os.path.dirname(self.doc_store_path), file))
        self.document_store = FAISSDocumentStore(sql_url=self.data_base_locations, embedding_dim=embedding_dim,
                                                 faiss_index_factory_str="Flat")
        docs = convert_files_to_docs(dir_path=self.doc_dir)
        docs = self.preprocessor.process(docs)
        self.document_store.delete_documents()
        self.document_store.write_documents(docs)

    def answer_question(self, query: str, k_retriver=10, k_reader=5):
        # return self.long_form_answering_pipe.run(
        #     query=query,
        #     params={"Retriever": {"top_k": k_retriver}, "Reader": {"top_k": k_reader}})

        return self.long_form_answering_pipe.run(
            query=query,
            params={"Retriever": {"top_k": 3}})

    def search_summary(self, query):
        self.summarizer.min_length = 200
        return self.search_summarizer_pipe.run(query=query, params={"Retriever": {"top_k": 20}})

    def generate_questions(self):
        pass

    def summarize_document(self):
        self.summaries.clear()
        for file in os.listdir(self.doc_dir):
            data = dict()
            data["file_name"] = file
            data["summary_data"] = list()
            with open(os.path.join(self.doc_dir, file)) as f:
                txt = f.read()
                paragraphs = txt.split('\n\n')
                for i, paragraph in enumerate(paragraphs):
                    paragraph_data = dict()
                    doc = Document(paragraph)
                    print("=================")
                    doc = self.preprocessor.process(doc)
                    summary = self.summarizer.predict(doc)
                    bullet_points = OpenAi.make_slide_point(summary)
                    paragraph_data["paragraph"] = paragraph
                    paragraph_data["summary"] = summary
                    paragraph_data["bullet points"] = bullet_points
                    data["summary_data"].append(paragraph_data)
                    if i > 2:
                        break
            self.summaries.append(data)
            break
        with open('summaries.json', 'w') as f:
            json.dump(self.summaries, f, indent=4, sort_keys=True)

    def fine_tune_reader(self):
        self.reader.train(data_dir=self.doc_dir, train_filename="dev-v2.0.json", use_gpu=True, n_epochs=1, save_dir="my_model")

    def fetch_github_documents(self):
        g = Github("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")
        out = g.get_repo("IanSullivan/OpenTextbook")
        contents = out.get_contents("/{}".format(self.agent_subject))
        for content_file in contents:
            url = content_file.download_url
            res = req.get(url)
            title = content_file.name
            raw_text = res.content.decode()
            title = title.replace(" ", "_")
            title = title.replace("?", "")
            title = title.replace(":", " ")
            file_name = str(title) + '.txt'
            with open(os.path.join(self.doc_dir, file_name), 'w') as f:
                f.write(raw_text)


if __name__ == "__main__":
    agent = Agent("Philosophy", init_db=False)
    answer = agent.answer_question("Who was Socrates?")
    print(answer)

