from djongo import models


class Reply(models.Model):
    auther = models.CharField(max_length=64)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Message(models.Model):
    auther = models.CharField(max_length=64)
    text = models.TextField()
    Reply = models.ArrayField(Reply, null=True)
    created_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PrivateChatRoom(models.Model):
    _id = models.ObjectIdField()
    sender = models.CharField(max_length=64)
    receiver = models.CharField(max_length=64, unique=True)
    message = models.ArrayField(Message)
    created_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(auto_now_add=True)
    objects = models.DjongoManager()
