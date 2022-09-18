import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.db.models import Q
from django.shortcuts import get_object_or_404

from account.models import User
from chat.models import PrivateChatRoom, Message


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['username']
        self.chat = await self.get_chat(self.user, user2)
        self.chat_id = f'chat_{self.chat.pk}'

        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
            })

    async def websocket_disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )

    async def websocket_receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data = json.dumps(text_data)
            text_data_json = json.loads(text_data)
            message = json.loads(text_data_json['text'])
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            msg = json.dumps({'type': 'msg', 'message': message, 'username': username})

            await self.create_message(message)
            await self.channel_layer.group_send(
            self.chat_id, {
                'type': 'chat_message',
                'message': msg,
                }
            )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    @database_sync_to_async
    def create_message(self, text):
        room = get_object_or_404(PrivateChatRoom, pk=self.chat.pk)
        message = Message(auther=self.scope['user'].username, text=text['text'], room=room)
        message.save()

    @database_sync_to_async
    def get_chat(self, user, user2):
        chat = PrivateChatRoom.objects.filter(
            Q(user1=user.username, user2=user2) | Q(user2=user.username, user1=user2)
        ).first()
        return chat
