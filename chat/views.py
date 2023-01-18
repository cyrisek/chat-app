from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Contact, Post
from .serializers import ChatSerializer
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()


def index(request):
    # Check for user authentication, if not send to login menu
    if request.user.is_authenticated:
        contacts = Contact.objects.all()

        context = {"contacts": contacts}
        return render(request, "chat/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))


def chat(request, id, name):
    user = request.user
    contacts = Contact.objects.all()
    print(id, user)
    # get contacts ID
    get_contact_reciver = contacts.get(id=id)
    get_contact_sender = contacts.get(user=user)
    chatterss = [get_contact_reciver.id, get_contact_sender.id]

    print(chatterss)
    print(get_contact_reciver.id)
    print(get_contact_sender.id)

    # get or create Chat
    chats = Chat.objects.filter(chatters=get_contact_reciver.id)
    chats2 = chats.filter(chatters=get_contact_sender.id)
    print(chats)
    print(chats2)
    if chats2.exists():
        print("yay")
        pass
    else:
        print("nay")
        chats2 = Chat.objects.create()
        chats2.chatters.set(chatterss)
        chats2.save()
    # establish what posts to render and chatID for websocket
    try:
        post_ids = chats2.values('posts')
        # print(post_ids.values_list('posts'))
        ids = post_ids.values_list('posts')
        all_posts = Post.objects.filter(id__in=ids)
        # print(all_posts)
        sender = all_posts.filter(author=get_contact_sender)
        reciver = all_posts.filter(author=get_contact_reciver)
        # print(sender, reciver)
        room_name = f"{chats2[0]}"
        print(room_name)
        # pagination
        paginator = Paginator(all_posts, 20)
        last_page = paginator.page_range.stop
        page = request.GET.get('page')
        if page is not None:
            all_posts = paginator.get_page(page)
            pass
        else:
            all_posts = paginator.get_page(last_page)
            pass
        return render(request, "chat/chat.html", {
            "room_name": room_name,
            "user": user,
            "contacts": contacts,
            "chats": chats,
            "all_posts": all_posts,
            "sender": sender,
            "reciver": reciver,
            "get_contact_reciver": get_contact_reciver
        })

    except:
        room_name = chats2
        print(room_name)
        return render(request, "chat/chat.html", {
            "room_name": room_name,
            "user": user,
            "contacts": contacts,
            "chats": chats,
            "get_contact_reciver": get_contact_reciver
        })


class ChatList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ChatDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# login and register
@ csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            contact = Contact.objects.get(user=user)
            contact.last_login = timezone.now()
            contact.status = 'active'
            contact.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")


def logout_view(request):
    user = request.user
    print(user)
    # Set contact to offline
    contact = Contact.objects.get(user=user)
    contact.status = 'inactive'
    contact.save()
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image = request.POST["imgUrl"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            print(user)
            #  Create new contact and set status to active
            contact = Contact.objects.create(
                user=user, last_login=timezone.now(), status='active', profile_img=image)
            contact.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")
