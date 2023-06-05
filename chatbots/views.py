from django.shortcuts import render

# Create your views here.
import pinecone

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from langchain.document_loaders import WebBaseLoader, NotionDirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, SpacyTextSplitter
from langchain.vectorstores import Pinecone

from .models import ChatBot
from .serializer import ChatBotSerializer
from .filters import IsOwner

from urllib.request import urlopen
import xml.etree.ElementTree as et
import json


# PINECONE_API_KEY = "1a89757e-91fa-420a-8fbc-6a39ff91da1d"
# PINECONE_ENV = "us-west4-gcp"

PINECONE_API_KEY = "3336e836-787e-49d4-8fd9-830ff614f160"
PINECONE_ENV = "us-west4-gcp-free"

class ChatBotViewSet(ModelViewSet):
    queryset = ChatBot.objects.all()
    serializer_class = ChatBotSerializer
    authentication_classes = [TokenAuthentication]
    filter_backends = [IsOwner]
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        print("inja")

        result = super().create(request, *args, **kwargs)

        website_urls = request.data['data']['website_urls']

        loader = WebBaseLoader(web_path=website_urls)
        raw_documents = loader.load()
        raw_documents = []

        # notion_loader = NotionDirectoryLoader('challenge-data/')

        # print("notion", notion_loader.load())
        
        # raw_documents.extend(notion_loader.load())

        text_splitter = SpacyTextSplitter(
            chunk_size=1000,
        )

        uuid = result.data['uuid']

        documents = text_splitter.split_documents(raw_documents)
        embeddings = OpenAIEmbeddings(openai_api_key="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")

        pinecone.init(
            api_key=PINECONE_API_KEY,  # find at app.pinecone.io
            environment=PINECONE_ENV  # next to api key in console
        )

        index_name = uuid

        try:
            pinecone.create_index(
                name=index_name,
                dimension=1536,
                metric='cosine',
            )

            _ = Pinecone.from_documents(documents, embeddings, index_name=index_name)
        except Exception as e:
            print("======================================", e )

        return result


class ExtractURLView(APIView):
    def post(self, request, format=None):
        with urlopen(request.data["xml_map"]) as url:
            data = url.read()

        xml = et.fromstring(data)
        nsmp = {"doc": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            
        urls = [url.find('doc:loc', namespaces = nsmp).text for url in xml.findall('doc:url', namespaces = nsmp)] 
        return Response(urls)
