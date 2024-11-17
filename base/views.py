
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Messages
from .forms import roomForm, UserForm
from django.contrib import messages
from django.http import HttpResponse

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username not found")
            return render(request, 'base/loginRegister.html', {'page': page})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home on successful login
        else:
            messages.error(request, "Username or Password is invalid")

    context = {'page': page}
    return render(request, 'base/loginRegister.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')

    context={'form':form}
    return render(request,'base/loginRegister.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(Host__username__icontains=q)
        )
    topics=Topic.objects.all()
    roomCount=rooms.count()
    roomMessages=Messages.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'roomCount':roomCount, 'roomMessages':roomMessages}
    return render(request, 'base/Home.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    roomMessages=user.messages_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'roomMessages':roomMessages,'topics':topics}
    return render(request,'base/profile.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    roomMessages=room.messages_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message = Messages.objects.create(
            users=request.user,
            room=room,
            body=request.POST.get('body')
        ) 
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context={'room':room, 'roomMessages':roomMessages, 'participants': participants}
    return render(request, 'base/Room.html', context)

@login_required(login_url='login')
def create_room(request):
    form=roomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        # form=roomForm(request.POST)
        topic_name=request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            Host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')   
    context={'form':form, 'topics': topics}
    return render(request,'base/Room_form.html',context)

@login_required(login_url='login')
def update_room(request, pk):
    room=Room.objects.get(id=pk)
    form=roomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.Host:
        return HttpResponse('You cant make changes to this room!')
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form, 'topics': topics, 'room':room}
    return render(request, 'base/Room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def delete_message(request, pk):
    msg=Messages.objects.get(id=pk)
    if request.method=='POST':
        msg.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':msg})

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form}
    return render(request, 'base/Update-user.html', context)