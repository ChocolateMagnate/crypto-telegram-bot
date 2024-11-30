import json
import asyncio

import openai
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from bot import logger, CRYPTO_PROJECTS_PATH


class LLM:
    def __init__(self, model: str, openai_api_key: str, temperature: float = 0.9):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature
        )

        with open(CRYPTO_PROJECTS_PATH, "r") as file:
            data = json.load(file)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.create_documents(data)
        vectorstore = FAISS.from_documents(chunks, embeddings)

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory
        )

    async def respond(self, text: str, max_rate_retries: int = 10) -> str:
        for attempt in range(max_rate_retries):
            try:
                response = await self.chain.ainvoke({"question": text})
                return response["answer"]
            except openai.RateLimitError as e:
                logger.error(f"Attempt #{attempt}: {e}")
                if attempt < max_rate_retries - 1:  # Don't sleep on last attempt
                    await asyncio.sleep(min(2 ** attempt, 32))  # Cap at 32 seconds
                    continue
            except openai.APIError as e:
                logger.error(f"OpenAI API error: {e}")
                return "OpenAI API is down. Please check status.openai.com"
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return "An error occurred while processing your request"
        return "Rate limit exceeded after multiple retries. Please try again later."
