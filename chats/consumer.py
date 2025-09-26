import json

from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print("Consumer connected!")
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        print("Consumer disconnected!")
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        self.close(code=close_code)

    def receive(self, text_data: str):
        print("Object recieved!")
        json_data = json.loads(text_data)
        user = json_data.get("user")
        if user:
            async_to_sync(self.channel_layer.group_send)(
                "chat",
                {
                    "type": "chat.message",
                    "user": user,
                    "date": timezone.now().isoformat(),
                    "text": json_data.get("text"),
                },
            )
        else:
            print("Not authorized!")
            self.close()

    def chat_message(self, event: dict):
        print("Message sent!")
        answer = f"{event["date"]} -> {event["user"]["username"]} -> {event["text"]}"
        self.send(text_data=answer)
