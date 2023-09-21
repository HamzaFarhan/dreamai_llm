from imports import *


def vllm(
    model_name,
    model_url="http://localhost:8000/v1",
    top_k=10,
    top_p=0.4,
    max_tokens=64,
    presence_penalty=0.4,
    frequency_penalty=0.6,
    length_penalty=0.7,
    model_kwargs={"stop": ["[END]", "\n\n"]},
):
    return VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=model_url,
        model_name=model_name,
        top_k=top_k,
        top_p=top_p,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        length_penalty=length_penalty,
        model_kwargs=model_kwargs,
    )


def run_llm(llm, prompt, template=None):
    if template is None:
        return llm(prompt)["text"].strip()
    chain = LLMChain(prompt=template, llm=llm)
    return chain(prompt)["text"].strip()


async def arun_llm(llm, prompt, template=None):
    if template is None:
        return await llm.acall(prompt)  # ["text"].strip()
    chain = LLMChain(prompt=template, llm=llm)
    return await chain.acall(prompt)  # ["text"].strip()
