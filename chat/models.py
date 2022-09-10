from djongo import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class Message(BaseModel):
    pass


class PrivateChatRoom(BaseModel):
    pass
