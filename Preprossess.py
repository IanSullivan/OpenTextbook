# import os
# from haystack.utils import convert_files_to_docs
# from haystack.nodes import PreProcessor, TextConverter
# from haystack import Pipeline
# from haystack.pipelines.standard_pipelines import TextIndexingPipeline
# doc_dir = "data/textbooks/Philosophy/"
# dir_list = [doc_dir + f for f in os.listdir(doc_dir)]
# indexing_pipeline = Pipeline()
# text_converter = TextConverter()
# preprocessor = PreProcessor(
#     clean_empty_lines=True,
#     clean_whitespace=True,
#     clean_header_footer=False,
#     split_by="word",
#     split_length=100,
#     split_respect_sentence_boundary=True,
# )
# # docs = preprocessor.process(all_docs)
#
# indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
# indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
#
# indexing_pipeline.run(file_paths=dir_list)
import os
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor

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

indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
# indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])

doc_dir = "data/textbooks/Philosophy"
files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
documents = indexing_pipeline.run_batch(file_paths=files_to_index)
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
print(docs)
