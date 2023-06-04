from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Consumer has been connected!", self.scope['url_path']['kwargs']['chatbot_id'])
        return await super().connect()


    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        chatbot_id = self.scope['url_path']['kwargs']['chatbot_id']
        print("Something received in consumer", text_data, chatbot_id)
        return await super().receive(text_data, bytes_data, **kwargs)