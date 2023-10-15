from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
import math
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
# llm = OpenAI(model_name="text-curie-001", temperature=0)
llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":64})
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)


def multiplier(a, b):
    return str(math.pow(a, b))

def losslessCardName(string):
    # a, b = string.split(",")
    return string


def pot_odds(string):
    # a, b = string.split(",")
    return string


def get_hand_history(string):
    # a, b = string.split(",")
    return string

tools = [
    # Tool(
    #     name="Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events. You should ask targeted questions"
    # ),
    # Tool(
    #     name="Calculator",
    #     func=llm_math_chain.run,
    #     description="useful for when you need to answer questions about math"
    # ),
    # Tool(
    #     name="Strategy Finder",
    #     func=losslessCardName,
    #     description="useful for when you need to look up the the strategy of the hand, with the losssless hand value and the action history, "
    #                 "The input to this tool should be the lossless hand follow by the action history. "
    #                 "For example, `To8o f,f,f,r10,c` would be the input if you wanted to input ten eight off suit with players folding and a raise of 10, "
    #                 # "'Ao,To' would be ace ten off suited, '37o' would be 3o7o "
    # ),
    # Tool(
    #     name="Card Finder",
    #     func=losslessCardName,
    #     description="useful for when you need to look up the losssless value of the card in question, "
    #                 "The input to this tool should be a comma separated list names of the two cards you want. "
    #                 "For example, `Ks,Qs` would be the input if you wanted to input king of spade and the queen of spades, "
    #                 "'Ao,To' would be ace ten off suited, '37o' would be 3o7o "
    # ),
    # Tool(
    #     name="Pot odds",
    #     func=pot_odds,
    #     description="useful for calculating the pot odds of a lossless hand, The input would be the lossless hand name, "
    #                 "For example '3o7o', 3 of spades would be incorrect"
    # ),
    Tool(
        name="Get hand History",
        func=get_hand_history,
        description="convert this sentence to a comma seperated list of actions taken at the poker table, "
                    "The order players play in is under the gun,under the gun + 1, high jack cut-off small blind, big blind "
                    "An example output would be [f, f, f, c, r20, f]"
        # description="useful for calculating actions that have happened in the pre flop.  "
        #             "The input is comma separated list of all actions that have been played.  "
        #             "The position order is 'Under the gun' acts first, then the 'high jack', the 'cut off',  the 'small blind', and 'big blind' acts last"
        #             "For example 'I start off in the high jack, if folds to me and I raise 3 big blinds, "
        #             "it folds to the small blind and he calls, the big blind folds', would be [f, f, r3, f, c, f]."
    ),
    Tool(
        name="Confirm Right answer",
        func=get_hand_history,
        description="Two sentences are inputted, your job is to determine if the two sentences mean the same thing.  "
                    "The answer a number on a scale of 1 to 10, one being the senteces are completly different, 10 being"
                    "the two senteces are exactly the same."
        # description="useful for calculating actions that have happened in the pre flop.  "
        #             "The input is comma separated list of all actions that have been played.  "
        #             "The position order is 'Under the gun' acts first, then the 'high jack', the 'cut off',  the 'small blind', and 'big blind' acts last"
        #             "For example 'I start off in the high jack, if folds to me and I raise 3 big blinds, "
        #             "it folds to the small blind and he calls, the big blind folds', would be [f, f, r3, f, c, f]."
    )
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
# react = initialize_agent(tools, llm, agent="react-docstore", verbose=True)
# mrkl.run("I start with the Ace Ten of diamonds in the cutoff and under the gun plus 1 raises 5 blinds, high jack folds, I call, "
#          "small blind folds and the big blind and re raises to 10 big blinds")
# out = agent.run("I start with the Ace Ten of diamonds in the high jack and, it folds to me, I raise 5 blinds, small blind folds and the big blind and re raises to 10 big blinds")
out = agent.run("Do these sentence mean the same thing.  \"This framework generates embeddings for each input sentence.\"  \"Cows park on the left side of the road\"")
