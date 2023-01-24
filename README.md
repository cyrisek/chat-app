# Chat Application

### Video Demo: [Click me!](https://youtu.be/8Nm8n0Z2TBw)

## Technologies used:

- Python (Django)
- Javascript
- HTML
- CSS
- Bootstrap
- WebSockets
- Redis

## Description:

- My final project is a web chat application created using HTML, CSS, Python and Javascript. I've used Django web framework based in Python for the backend. The database is default sqlite3 using models. I've also used Bootstrap and CSS for styling purposes.
- Chat App is my version of Messenger. Messenger is a proprietary instant messaging app and platform developed by Meta Platforms. It is a generic chat app, that is using WebSocket for a real-time chat experience.

## Distinctiveness and Complexity:

- My project is a web chat application that utilizes a variety of technologies including HTML, CSS, Python, and JavaScript. The application utilizes a real-time chat experience using WebSockets, which provides a more seamless and interactive user experience compared to traditional, request-response based chat systems. This feature sets my application apart from other chat applications that rely on traditional request-response based communication.
- The backend of my application is built using the Django web framework, which is based on Python. I've also used Bootstrap and custom CSS for styling to create a visually appealing and user-friendly interface. Additionally, I've incorporated Django's built-in user authentication system, and I've added additional models such as Chat, Post, and Contact to support the functionality of the chat feature.
- The application is mobile-responsive, which allows for a consistent user experience across different devices. This is an important feature as more and more people are using their mobile devices to access the internet. By making the application mobile-responsive, I've ensured that users can access the application and use its features regardless of the device they're using.
- In summary, my project is unique in its implementation of real-time chat using WebSockets, the use of Django framework, and mobile responsiveness. These features, combined with the additional models, create a complex and dynamic application that stands out from other projects in the course. I believe that this project satisfies the distinctiveness and complexity requirements and I am proud of the effort and energy I have put into creating this application.

## How to Run the Application:

### Video Installation: [Click me!](https://youtu.be/Zpjn8Gnt9Tw)

### setup redis and install pipenv

- Make sure you have Python and Django installed on your codespace
- Clone the repository to your codespace or local machine
- sudo apt-get install redis (Redis is not officially supported on Windows. Here is more information about installing on Windows[Redis for windows](https://redis.io/docs/getting-started/installation/install-redis-on-windows/))

```
pip install pipenv
```

### Create a virtual environment

```
pipenv shell
```

#### install reaquirements.txt:

```
pip install -r requirements.txt
```

- redis-server(make sure Redis server is running on port: 6379)

#### run the app (you can use two commands together using & or just open 2 terminals):

```
redis-server & python manage.py runserver
```

## File Structure:

### chat/static/chat

#### /index.js

- In JavaScript first thing we do is create WebSocket that takes chat id as a roomName argument to create individual layers for each chat.

```
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);
```

- In case of a connection error it's sending a consol.log message and alert to the user.
- When sending a new message create a new document object that is segregated either to left or right, depending on whom sends the message.

```
 if (parseInt(data.user_id) === userID) {
        ul.innerHTML += ` <li class="clearfix">
        <div class="message-data">
            <span class="message-data-time">Just now.</span>
        </div>
        <div class="message my-message">${data.message}</div>
    </li>`;
    } else {
        ul.innerHTML += `<li class="clearfix">
            <div class="message-data text-right">
                <span class="message-data-time">Just now.</span>
            </div>
            <div class="message other-message float-right">${data.message}</div>
        </li>`;
    }
    scrollDown();
```

- When sending the message to Consumer.py it also sends chat_id and user_id so the message can be saved in the database.

```
 chatSocket.send(JSON.stringify({
        'message': message,
        'chat_id': chat_id,
        'user_id': user_id,
    }));
```

- Each time message is sent scrollDown function is triggered to make the user feel like the application is responsive.

#### /styles.css

- Contains styling of the HTML templates.

### chat/static/templates

#### /base.html

- Contains links to Bootstrap CDN, Google fonts, Bootstrap icons, static files and title.

#### /chat.html

- Shows chat template with messages between users. Create a user list on the left and generate current chat messages.

#### /index.html

- Shows a list of users you can choose to start a chat with.

#### /login.html

- login template.

#### /register.html

- register template.

### chat/

#### /consumers.py

- Contains ChatConsumer class that manages the WebsocketConsumer.
- While receiving the message, a New post object is created and added to the chat.

```
newPost = Post.objects.create(
            author=newAuthor,
            body=message)
```

- JSON data is sent back to the receiver so the message can appear on the right side of the chat app.

```
 self.send(text_data=json.dumps({
            "message": message,
            "chat_id": chat_id,
            "user_id": user_id,
        }))
```

#### /views.py

- Respectively, contains all application views.
- On the index page we are rendering only contacts that are appearing on the right side of the screen.

```
 if request.user.is_authenticated:
        contacts = Contact.objects.all()

        context = {"contacts": contacts}
        return render(request, "chat/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))
```

- When the Contact avatar is clicked, we are either getting a chat when chatters are users and contact or creating a new chat if the chat doesn't exist in the first place.
- Posts are being filtered for the ones that are in the chat and then further in jinja plates, we segregate them to left and right, depending if the user is the sender or receiver.
- Chat id is also being sent to the frontend as a room_name so we can get the id for the WebSocket port.
- Chat Url is constructed from contact id and user in a way that any other than your chats can't be accessed.
- There is also a chat API rest view set up at ....chat_api/ even though it's not used, it help me understand what was going on.
- When the User is registering, a contact profile is also created.

```
user = User.objects.create_user(username, email, password)
            user.save()
            print(user)
            #  Create new contact and set status to active
            contact = Contact.objects.create(
                user=user, last_login=timezone.now(), status='active', profile_img=image)
            contact.save()
```

- While login in user status is changed to online, and while login out user status is changed to offline.

```
 contact = Contact.objects.get(user=user)
            contact.last_login = timezone.now()
            contact.status = 'active'
            contact.save()
```

#### /models.py

- There are 3 models besides basic User(Contact, Post and Chat).

```
class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    last_login = models.DateTimeField(blank=True, null=True, editable=True)
    status = models.CharField(max_length=255, default='inactive')
    profile_img = models.CharField(
        max_length=255, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='author')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username



class Chat(models.Model):
    chatters = models.ManyToManyField(
        Contact, blank=True, related_name="chats")
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return "{}".format(self.pk)

```

- Chat is storing 2 contacts IDs and posts IDs that were sent during this chat.
  ![](images/chat.png)
- Contact model stores when the user last login, status(if a user is online or offline) and profile image.
  ![](images/contactmodel.png)
- Post model is storing the author of the post, body, and timestamp.
  ![](images/postmodel.png)

#### /admin.py

- Here I register three admin classes Chat, Contact, Post

#### /serializers.py

- Here I create serializers for my models.

#### /routing.py

- contains a unique URL for WebSocket connection that takes room_name argument.

#### /urls.py

- all application URLs.

### capstone/

#### /asgi.py

- Initialize Django ASGI application.

```
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
```

#### /settings.py

- I added installed apps.

### images/

- Contains images for README file.

## Additional Information:

- The application uses the default SQLite3 database, but it can be easily configured to use other databases such as PostgreSQL or MySQL.
- The application is currently deployed on a hosting platform, accessible via the following [URL](https://chat-app-cs50web.up.railway.app/). The deployment is powered by Nginx, a popular HTTP server software, ensuring reliable and efficient delivery of the application to users.

### CSS/Bootstrap

- Application was made using Bootstrap 5.
- Design is simple and supposed to resemble Messenger feel like.
- For a font family I am using Lato for a better user experience.
- Application is responsive and has simple animation.

## Credits

- WebSockets were installed using channels documentation [Channels](https://channels.readthedocs.io/)
- User avatars are random pictures from [Google](https://www.google.com/)
