from llm_utils import *
from prompt_templates import *


async def async_run_llm(llm, input, template=None):
    if template is None:
        return await llm.acall(input)
    chain = LLMChain(prompt=template, llm=llm)
    return await chain.acall(input)


async def async_ask_q(llm, prompt):
    res = await async_run_llm(llm, prompt, template=qna_template)
    print(f"\nQuestion: {prompt}\nAnswer: {res}\n")
    return res


async def async_complete_sentence(llm, prompt):
    res = await async_run_llm(llm, prompt, template=complete_template)
    print(f"\n{prompt} {res}\n")
    return res
