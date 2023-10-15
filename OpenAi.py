import openai
import re
from ast import literal_eval


def problem_set_eval(correct_answer, submitted_answer):
    prompt = """Grade the submitted answer on a scale of one to ten,  The correct answer is "{} "
the submitted answer is "{}"
Output should be the number, then followed by a hint if the answer is incorrect"
      """.format(correct_answer, submitted_answer)
    print(prompt)
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt)
    out = completion.choices[0].text
    matches = re.findall(r"[-+]?(?:\d*\.*\d+)", out)
    print(out.split(matches[0]))
    print(matches[0])


def make_slide_point(summarized_paragraph):
    prompt = """
    Take the following paragraph and convert it into bullet points for a slide show. Output should be a python list of 
    strings max length of 5:
    {}
    """.format(summarized_paragraph)
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200, temperature=0.2)
    out = completion.choices[0].text
    # print(completion)
    return literal_eval(out)


if __name__ == "__main__":
    real_answer = "The supply curve for Mexican textiles shifts to the left. This results in a higher equilibrium price and lower equilibrium quantity in the market for Mexican textiles."
    submit_answer = "The supply curve for textiles would shift left.  This would result in a higher equilibrium price and lower equilibrium quantity in the market  for Mexican textiles"
    problem_set_eval(real_answer, submit_answer)
