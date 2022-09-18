from django.urls import path

from chat.views import room_list, create_room, room

urlpatterns = [
    path('', room_list, name='room_list'),
    path('create/', create_room, name='room_create'),
    path('<str:username>/', room, name='room')
]
