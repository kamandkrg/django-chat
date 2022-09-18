import json

from bson import ObjectId
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from account.models import User
from chat.models import PrivateChatRoom, Message


@login_required
def room_list(request):
    user = request.user.username
    rooms = PrivateChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
    room = get_object_or_404(PrivateChatRoom, pk=1)
    Message.objects.create(room_id=room, auther=request.user, text='hi kamand')
    return render(request, 'chat/index.html', {'rooms': rooms})


def room(request, username):
    # if request.method == 'POST':
    #     room_id = request.POST.get('room_id')
    #     private_room = get_object_or_404(PrivateChatRoom, pk=room_id)
    #     message = request.POST.get('message')
    #     Message.objects.create(room=private_room, text=message, auther=request.user.username)
    #     return redirect('room')
    username1 = request.user.username
    room_private = PrivateChatRoom.objects.filter(
        Q(user1=username) | Q(user2=username),  Q(user1=username1) | Q(user2=username1)
    )

    if room_private.exists():
        return render(request, 'chat/room.html', {'room': room_private.first(), 'username': username,
                                                  'chat_id_json': mark_safe(json.dumps(username))})
    return redirect('room_list')


@login_required
@require_http_methods(['POST'])
def create_room(request):
    username = request.POST.get('username')
    get_object_or_404(User, username=username)
    username1 = request.user.username
    room = PrivateChatRoom.objects.filter(
        Q(user1=username) | Q(user2=username),  Q(user1=username1) | Q(user2=username1)
    )
    if room.exists():
        return redirect('room_list')
    PrivateChatRoom.objects.create(user1=username1, user2=username, message=[])
    return redirect('room_list')















