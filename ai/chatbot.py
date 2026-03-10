from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.2,
    streaming=True
)


prompt = PromptTemplate(
    template="""
You are a professional financial advisor.

Use the financial data below to answer the user's question.

Investment Summary
-------------------
Total Invested: {invested}
Future Corpus: {corpus}
Real Corpus: {real_corpus}
Total Withdrawn: {withdrawn}
Remaining Corpus: {remaining}

Explain clearly like a professional financial planner.

User Question:
{question},

If the question is not related to finance, simply reply with 'Ask finance related question, Please!', this will settle the hallucination.
""",
    input_variables=[
        "invested",
        "corpus",
        "real_corpus",
        "withdrawn",
        "remaining",
        "question"
    ]
)


chain = prompt | llm | StrOutputParser()


# Chat History Storage

store = {}


def get_session_history(session_id):

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


chat_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question"
)


def financial_chat_stream(user_question, data):

    return chat_chain.stream(
        {
            "invested": data["invested"],
            "corpus": data["corpus"],
            "real_corpus": data["real_corpus"],
            "withdrawn": data["withdrawn"],
            "remaining": data["remaining"],
            "question": user_question
        },
        config={"configurable": {"session_id": "finance_user"}}
    )