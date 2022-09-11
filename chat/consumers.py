import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self):
        self.user = self.scope['user']
        self.chat_id = f'chat_{self.user.pk}'

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.chat_id, {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
