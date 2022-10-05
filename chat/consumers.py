import json

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncConsumer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from account.models import User
from chat.models import PrivateChatRoom, Message


class ApplicationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.send(
                {'type': 'websocket.close'}
            )

        await self.channel_layer.group_add(
            self.user.username,
            self.channel_name
        )
        await self.send(
            {'type': 'websocket.accept'}
        )

    async def websocket_disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user.username,
            self.channel_name
        )
        raise StopConsumer()


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['username']
        self.chat = await self.get_chat(self.user.username, user2)
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
        raise StopConsumer()

    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        bytes_data = event.get('bytes', None)

        if text_data is not None:
            text_data_json = json.loads(text_data)
            text = text_data_json['text']
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            msg = json.dumps({'type': 'msg', 'text': text, 'username': username})

            await self.create_message(text)
            await self.channel_layer.group_send(
            self.chat_id, {
                'type': 'chat_message',
                'message': msg,
                'sender_channel_name': self.channel_name
                }
            )

    async def chat_message(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send({
                'type': 'websocket.send',
                'text': event['message']
            })

    @database_sync_to_async
    def create_message(self, text):
        room = get_object_or_404(PrivateChatRoom, pk=self.chat.pk)
        message = Message.objects.create(auther=self.scope['user'], text=text, room=room)
        return message

    @database_sync_to_async
    def get_chat(self, user, user2):
        user1 = get_object_or_404(User, username=user)
        user_2 = get_object_or_404(User, username=user2)
        chat = PrivateChatRoom.objects.filter(
            Q(user1=user1, user2=user_2) | Q(user2=user1, user1=user_2)
        ).first()

        return chat
