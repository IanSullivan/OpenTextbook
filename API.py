from fastapi import FastAPI
from Agent import Agent

# initialize API
app = FastAPI()

AI_subjects = {'Philosophy': Agent("Philosophy", init_db=False)}


@app.get('/query/')
async def get_query(query: str, subject: str, retriever_limit: int=10, reader_limit: int=3):
    """Makes query to doc store via Haystack pipeline.
    :param qeury: Query string representing the question being asked.
    :type qeury: str
    """
    return AI_subjects["Philosophy"].answer_question(query, retriever_limit, reader_limit)


@app.get('/summary/')
async def get_query(query: str, subject:str, retriever_limit: int=10, reader_limit: int=3):
    """Makes summary from the doc store via Haystack pipeline.
    :param qeury: Query string representing the question being asked.
    :type qeury: str
    """
    return AI_subjects["Philosophy"].search_summary(query)
