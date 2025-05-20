from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q
from datetime import date
from django.shortcuts import get_object_or_404
from .forms import Register_User_Form

from .forms import RoomForm
from .models import Room, Topic, Message


def login_page(request):
    page = 'login_page'
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login_page')
    else:
        return render(request, "wydarzenia/login_page.html", {"page": page})


def logout_user(request):
    logout(request)
    return redirect("home")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = Register_User_Form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,('Rejestracja zakończona pomyślnie!'))
            return redirect("home")
    else:
        form = Register_User_Form()

    return render(request, "wydarzenia/register_page.html", {"form": form})


def home(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q),
        date__gte=date.today(),
    ).order_by("date")
    return render(
        request,
        "wydarzenia/home.html",
        {
            "room_list": rooms,
            "topics": Topic.objects.all(),
            "room_count": rooms.count(),
            "active_topic": q,
        },
    )


def history(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q),
        date__lt=date.today()
    ).order_by("-date")
    return render(
        request,
        "wydarzenia/history.html",
        {
            "room_list": rooms,
            "topics": Topic.objects.all(),
            "room_count": rooms.count(),
            "active_topic": q,
        },
    )


def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all().order_by("-created")

        if request.method == "POST":
            message = Message.objects.create(
                user=request.user, room=room, body=request.POST.get("body")
            )
            return redirect("room", pk=room.id)
        return render(
            request,
            "wydarzenia/room.html",
            {"room": room, "room_messages": room_messages},
        )
    except Room.DoesNotExist:
        return render(
            request,
            "404.html",
            {"my_var": "The Room You Are Looking For Does Not Exists"},
        )


def profile(request, pk):
    try:
        profile = User.objects.get(id=pk)
        room_list_by_date = Room.objects.filter(host=pk).order_by("date")
        return render(
            request,
            "wydarzenia/profile.html",
            {
                "profile": profile,
                "topics": Topic.objects.all(),
                "room_list": room_list_by_date,
            },
        )
    except User.DoesNotExist:
        return render(request, "404.html", {"my_var": "User Does Not Exists"})


@login_required(login_url="login_page")
def create_room(request):
    submitted = False
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return HttpResponseRedirect("/create-room?submitted=True")
    else:
        form = RoomForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "wydarzenia/room_form.html", {"form": form, 'submitted': submitted})


@login_required(login_url="login_page")
def update_room(request, pk):
    try:
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        if room.host == request.user:
            if request.method == "POST":
                form = RoomForm(request.POST, instance=room)
                if form.is_valid():
                    form.save()
                    return redirect("home")
            return render(request, "wydarzenia/room_form.html", {"form": form})
        else:
            return render(request, "403.html")
    except Room.DoesNotExist:
        return render(
            request,
            "404.html",
            {"my_var": "The Room You Want To Update Does Not Exists"},
        )


@login_required(login_url="login_page")
def delete_room(request, pk):
    try:
        room = Room.objects.get(id=pk)
        if room.host == request.user:
            if request.method == "POST":
                room.delete()
                return redirect("home")
            return render(request, "wydarzenia/delete.html", {"obj": room})
        else:
            return render(request, "403.html")
    except Room.DoesNotExist:
        return render(
            request,
            "404.html",
            {"my_var": "The Room You Want To Delete Does Not Exists"},
        )


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect("room",message.room.id)
    return render(request, "wydarzenia/delete.html", {"obj": message})


def error_500(request):
    return render(request, "500.html")


def error_404(request, exception):
    return render(request, "404.html")
