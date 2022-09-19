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
    user = get_object_or_404(User, username=request.user.username)
    rooms = PrivateChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
    return render(request, 'chat/index.html', {'rooms': rooms})


def room(request, username):
    username2 = get_object_or_404(User, username=username)
    username1 = get_object_or_404(User, username=request.user.username)
    room_private = PrivateChatRoom.objects.filter(
        Q(user1=username2) | Q(user2=username2),  Q(user1=username1) | Q(user2=username1)
    )

    if room_private.exists():
        return render(request, 'chat/room.html', {'room': room_private.first(), 'username': username,
                                                  'chat_id_json': mark_safe(json.dumps(username))})
    return redirect('room_list')


@login_required
@require_http_methods(['POST'])
def create_room(request):
    user1 = request.POST.get('username')
    username = get_object_or_404(User, username=user1)
    username1 = get_object_or_404(User, username=request.user.username)
    pv_room = PrivateChatRoom.objects.filter(
        Q(user1=username) | Q(user2=username),  Q(user1=username1) | Q(user2=username1)
    )
    if not pv_room.exists():
        PrivateChatRoom.objects.create(user1=username1, user2=username)
    return redirect('room_list')















