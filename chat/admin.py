from django.contrib import admin

from .models import Contact, Chat, Post

admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Post)
