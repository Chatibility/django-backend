import pinecone
import json

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from .callback import QuestionGenCallbackHandler, StreamingLLMCallbackHandler
from .query_data import get_chain
from .schemas import ChatResponse

PINECONE_API_KEY = "8b1bc6f0-bf61-487e-ba8c-0ecc54607ebc"
PINECONE_ENV = "us-west4-gcp-free"


def to_json(resp):
    return {
        "sender": resp.sender,
        "message": resp.message,
        "type": resp.type
    }


class ChatConsumer(AsyncWebsocketConsumer):

    chat_histories = {}
    qa_chains = {}

    async def websocket_connect(self, message):
        chat_id = str(self.scope['url_route']['kwargs']['chat_id'])

        pinecone.init(
            api_key=PINECONE_API_KEY,  # find at app.pinecone.io
            environment=PINECONE_ENV  # next to api key in console
        )

        docsearch = Pinecone.from_existing_index(chat_id, OpenAIEmbeddings(openai_api_key="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"))

        question_handler = QuestionGenCallbackHandler(self)
        stream_handler = StreamingLLMCallbackHandler(self)

        qa_chain = get_chain(docsearch, question_handler, stream_handler)


        self.qa_chains[self.channel_name] = qa_chain
        self.chat_histories[self.channel_name] = []

        return await super().websocket_connect(message)

    async def connect(self):
        return await super().connect()


    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        await super().receive(text_data, bytes_data, **kwargs)
        
        chat_id = str(self.scope['url_route']['kwargs']['chat_id'])
        question = text_data

        resp = ChatResponse(sender="you", message=question, type="start")
                

        await self.send(json.dumps(resp.dict()))

        start_resp = ChatResponse(sender="bot", message="", type="start")
        await self.send(json.dumps(start_resp.dict()))

        qa_chain = self.qa_chains[self.channel_name]
        chat_history = self.chat_histories[self.channel_name]

        result = await qa_chain.acall(
                {"question": question, "chat_history": chat_history}
        )

        self.chat_histories[self.channel_name].append((question, result["answer"]))
        end_resp = ChatResponse(sender="bot", message="", type="end")

        await self.send(json.dumps(end_resp.dict()))


    async def disconnect(self, code):
        return await super().disconnect(code)
