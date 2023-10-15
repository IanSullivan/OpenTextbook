import os

from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor
from haystack.nodes import EmbeddingRetriever
from haystack.nodes import BM25Retriever

from haystack.document_stores import InMemoryDocumentStore
from haystack.document_stores import FAISSDocumentStore

from haystack.nodes import FARMReader

from haystack.pipelines import ExtractiveQAPipeline
from haystack.pipelines.standard_pipelines import TextIndexingPipeline


doc_dir = "data/build_your_first_question_answering_system"
files_to_index = [[doc_dir + "/" + f for f in os.listdir(doc_dir)][0]]
indexing_pipeline = Pipeline()
text_converter = TextConverter()
preprocessor = PreProcessor(
    clean_whitespace=True,
    clean_header_footer=True,
    clean_empty_lines=True,
    split_by="word",
    split_length=200,
    split_overlap=20,
    split_respect_sentence_boundary=True,
)

# document_store = InMemoryDocumentStore(use_bm25=True)
document_store = InMemoryDocumentStore(use_bm25=False)

# document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")
indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
# indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])
# indexing_pipeline.run(files_to_index)

indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_format="sentence_transformers",
)

document_store.update_embeddings(retriever)
# retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
pipe = ExtractiveQAPipeline(reader, retriever)

prediction = pipe.run(
    query="Who created the Dothraki vocabulary?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
)

print(prediction)
