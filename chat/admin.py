from django.contrib import admin
from chat.models import PrivateChatRoom, Message

# @register(PrivateChatRoom)
# class Chat(admin.ModelAdmin):
#     list_display = ('created_time', )

admin.site.register(PrivateChatRoom)
admin.site.register(Message)