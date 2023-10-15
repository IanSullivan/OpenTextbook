from langchain import HuggingFaceHub, LLMChain
from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
# initialize Hub LLM
import math

template = """Question: {question}
def 
Answer: """

def multiplier(a, b):
    return str(math.pow(a, b))

def parsing_multiplier(string):
    a, b = string.split(",")
    return multiplier(int(a), int(b))

# llm = OpenAI(temperature=0)
# llm = OpenAI(temperature=1e-10, model_name='text-davinci-002')
llm = HuggingFaceHub(repo_id="gpt2")
print(llm("Tell me a funny joke"))
# llm = HuggingFaceHub(
#         repo_id='google/flan-t5-xl',
#         model_kwargs={'temperature': 1e-10},
# )
# db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

# print(db_chain.run("How many employees are there?"))
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    # Tool(
    #     name="Calculator",
    #     func=llm_math_chain.run,
    #     description="useful for when you need to answer questions about math"
    # ),
    Tool(
        name="Multiplier",
        func=parsing_multiplier,
        description="useful for when you need to find the power of two numbers together. The input to this tool should be a comma separated list of numbers of length two, representing the two numbers you want to power together. For example, `1,2` would be the input if you wanted to multiply 1 ^ 2."
    )
]

# create prompt template > LLM chain
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)
response = agent({"input": "How championships have the bluejays won raised to the 23 power?"})
# out = agent.run("How old is Olivia Wilde's boyfriend? What is that number raised to the 0.23 power?")
# print(out + " clam")
print(response)