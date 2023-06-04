from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, UUIDField  

from .models import ChatBot

class ChatBotSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    uuid = UUIDField(read_only=True)

    class Meta:
        model = ChatBot
        fields = ['name', 'website_url', 'user', 'uuid']