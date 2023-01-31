# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Post, Chat, Contact


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room groupa
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    # Receive message from WebSocket

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json["chat_id"]
        user_id = text_data_json["user_id"]

        # create new post
        newAuthor = Contact.objects.get(user=user_id)
        print(newAuthor)
        newPost = Post.objects.create(
            author=newAuthor,
            body=message)
        chat = Chat.objects.filter(id=chat_id)
        chat[0].posts.add(newPost)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message", "message": message,
                "chat_id": chat_id,
                "user_id": user_id,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        chat_id = event["chat_id"]
        user_id = event["user_id"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "chat_id": chat_id,
            "user_id": user_id,
        }))
