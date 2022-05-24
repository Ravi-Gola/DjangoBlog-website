from django.contrib import admin
from .models import Contact
from.models import Post
from .models import Blogcomment

# Register your models here.
admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(Blogcomment)
