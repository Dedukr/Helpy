from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .models import Room, Topic, Message
from .form import RoomForm, UserForm
from django.views.generic import (
    View,
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

# Create your views here.


@login_required(login_url="login")
def profile_view(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    activity = user.message_set.all().order_by("-updated", "-created")
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms_list": rooms,
        "topics": topics,
        "activity": activity,
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def profile_edit_view(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        user.email = request.POST.get("email")
        user.username = request.POST.get("username")
        user.save()
        return redirect("profile", pk=request.user.id)

    context = {"user": user, "form": form}
    return render(request, "profile_edit.html", context)


def register_view(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect("rooms-list")
    context = {"form": form}

    return render(request, "register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("rooms-list")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does Not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("rooms-list")
        if messages.error:
            messages.error(request, "Username or password is incorrect")

    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("rooms-list")


def topics_list_view(request):
    q = request.GET.get("q") or ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, "topics.html", context)


def activities_list_view(request):
    q = request.GET.get("q") or ""
    messages = Message.objects.filter(
        Q(user__username__icontains=q)
        | Q(text__icontains=q)
        | Q(room__topic__name__icontains=q)
    ).order_by("-updated", "-created")

    context = {"activity": messages}
    return render(request, "activity.html", context)


def rooms_list_view(request):
    q = request.GET.get("q") or ""
    queryset = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    rooms_count = queryset.count()
    activity = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by(
        "-updated", "-created"
    )
    topics = Topic.objects.all()[:5]
    context = {
        "rooms_list": queryset,
        "topics": topics,
        "filtered_rooms_count": rooms_count,
        "activity": activity,
    }
    return render(request, "rooms/home.html", context)


def room_detail_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()
    if request.method == "POST":
        Message.objects.create(
            user=request.user, room=room, text=request.POST.get("text")
        )
        room.participants.add(request.user)
        return redirect("rooms-detail", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "rooms/rooms_detail.html", context)


@login_required(login_url="login")
def room_create_view(request):
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            name=request.POST.get("name"),
            topic=topic,
            description=request.POST.get("description"),
        )
        room.save()
        room.participants.add(request.user)
        return redirect("rooms-list")

    topics = Topic.objects.all()
    context = {"topics": topics}
    return render(request, "rooms/rooms_create.html", context)


@login_required(login_url="login")
def room_update_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("rooms-list")

    context = {"topics": topics, "room": room}
    return render(request, "rooms/rooms_create.html", context)


@login_required(login_url="login")
def room_delete_view(request, pk):
    obj = get_object_or_404(Room, id=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("rooms-list")
    context = {"object": obj}
    return render(request, "delete.html", context)


@login_required(login_url="login")
def message_delete_view(request, pk, id):
    message = get_object_or_404(Message, id=id)
    if request.method == "POST":
        message.delete()
        return redirect(message.room.get_absolute_url(), kwargs={"pk": pk})
    context = {"object": message}
    return render(request, "delete.html", context)
