from langchain import PromptTemplate, HuggingFaceHub, LLMChain

template = """Semmantic Similarity: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature": 0, "max_length":64}))


# question = "Do these sentence mean the same thing.  \"This framework generates embeddings for each input sentence.\"  \"Cows park on the left side of the road\""
correct_answer = "The supply curve for Mexican textiles shifts to the left. This results in a higher equilibrium price and lower equilibrium quantity in the market for Mexican textiles."
# submitted_answer = "The supply curve for Mexican textiles shifts to the left. This results in a higher equilibrium price and lower equilibrium quantity in the market for Mexican textiles."
# submitted_answer = "The supply curve would shift left.  This would result in a higher price and lower equilibrium quantity in the market  for Mexico textiles"
submitted_answer = "This framework generates embeddings for each input sentence."
prompt = """On a scale of one to ten do these senteces mean the same thing, one being the answers are completly different, ten being the senteces are the same  The correct answer is "{} "
the submitted answer is "{}"
Output should be the integer followed by a hint if the answer is incorrect"
      """.format(correct_answer, submitted_answer)
print(prompt)
print(llm_chain.run(prompt))