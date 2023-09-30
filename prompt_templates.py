from imports import *

qna_template = PromptTemplate.from_template(
    "Answer this question and add [END] to the end:\nQuestion: {question}\nAnswer:"
)

complete_template = PromptTemplate.from_template(
    "Complete this sentence and add [END] to the end: {text}"
)
