from imports import *
from prompt_templates import *


def vllm_client(
    model_name,
    model_url="http://localhost:8000/v1",
    top_k=10,
    top_p=0.4,
    max_tokens=64,
    presence_penalty=0.4,
    frequency_penalty=0.6,
    length_penalty=0.7,
    model_kwargs={"stop": ["[END]", "\n\n"]},
    **kwargs,
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
        **kwargs,
    )


def openai_client(openai_api_key, temperature=0, max_tokens=500, **kwargs):
    return OpenAI(
        openai_api_key=openai_api_key, temperature=temperature, max_tokens=max_tokens, **kwargs
    )


def openai_chat_client(
    openai_api_key, model_name="gpt-3.5-turbo", temperature=0, max_tokens=500, **kwargs
):
    return ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )


llm_fn_dict = {"vllm": vllm_client, "openai": openai_client, "openai_chat": openai_chat_client}


def run_llm(llm, prompt, template=None):
    if template is None:
        return llm(prompt)["text"].strip()
    chain = LLMChain(prompt=template, llm=llm)
    return chain(prompt)["text"].strip()


def ask_q(llm, prompt):
    res = run_llm(llm, prompt, template=qna_template)
    print(f"\nQuestion: {prompt}\nAnswer: {res}\n")
    return res


def complete_sentence(llm, prompt):
    res = run_llm(llm, prompt, template=complete_template)
    print(f"\n{prompt} {res}\n")
    return res
