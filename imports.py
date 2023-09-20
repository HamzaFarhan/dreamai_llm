from ray import serve
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from langchain.llms import VLLMOpenAI
from fastapi.responses import JSONResponse
from langchain import PromptTemplate, LLMChain
