from django.db.models import Q

from account.models import User
from django.db import models


class StatusMessage(models.Model):
    STATUS_CHOICE = (
        (0, 'not delivered'),
        (1, 'delivered'),
        (2, 'seen')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_messages')
    status = models.IntegerField(choices=STATUS_CHOICE, default=0)


class PinChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
    status = models.BooleanField(default=False)


class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='private_room_sender')
    user2 = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='private_room_receiver')
    pin = models.ForeignKey(PinChat, on_delete=models.SET_NULL, null=True, related_name='chats')
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    def get_messages(self):
        return self.messages.all()


class Message(models.Model):

    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    reply_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='parent')
    text = models.TextField()
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name='messages')
    status = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
