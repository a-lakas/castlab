import os
import chainlit as cl
import langchain
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
import streamlit as st
import asyncio

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = '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'

repo_id = 'tiiuae/falcon-7b-instruct'

llm = HuggingFaceHub(huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
                     repo_id=repo_id,
                     model_kwargs={"temperature": 0.6, "max_new_tokens": 500})

template = """Question: {question}

Answer: Let's give you a well-informed answer."""

@cl.on_chat_start
async def main():
    elements = [
        cl.Image(name='falcon-llm.jpeg', display='inline', path='../falcon7b-instruct-chat/falcon-llm.jpeg')
    ]
    await cl.Message(content="Hello there, I am Falcon 7b Instruct. How can I help you?", elements=elements).send()
    prompt = PromptTemplate(template=template, input_variables=['question'])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    cl.user_session.set('llm_chain', llm_chain)

@cl.on_message
async def main(message: str):
    llm_chain = cl.user_session.get('llm_chain')

    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    return res['text']

# Streamlit App
st.title("Falcon 7b Instruct Chat")
user_input = st.text_input("Ask a question:")

if user_input:
    result_placeholder = st.empty()
    result = await main(user_input)
    result_placeholder.text(result)
