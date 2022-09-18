from djongo import models


class PrivateChatRoom(models.Model):
    user1 = models.CharField(max_length=64)
    user2 = models.CharField(max_length=64, unique=True)
    stare = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}"


class Message(models.Model):
    auther = models.CharField(max_length=64)
    text = models.TextField()
    Reply = models.ArrayReferenceField("self", on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    room = models.ArrayReferenceField(to=PrivateChatRoom, on_delete=models.CASCADE, related_name='messages')
    modify_time = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=False)





