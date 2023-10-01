from imports import *

industry_problem_template = PromptTemplate.from_template(
    """I want you to act as a business partner.
    I work in {industry} and one of our key challenges is {problem}.
    I believe there's an opportunity here, but I need fresh ideas. Help me brainstorm 5 innovative solutions or approaches to address this long-standing challenge effectively."""
)

qna_template = PromptTemplate.from_template(
    "Answer this question and add [END] to the end:\nQuestion: {question}\nAnswer:"
)

complete_template = PromptTemplate.from_template(
    "Complete this sentence and add [END] to the end: {text}"
)
