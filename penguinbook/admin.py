from django.contrib import admin
from .models import User, Profile #, Post, Friend, Profile,
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .form import RegistrationForm
# Register your models here.

admin.site.unregister(  User)
admin.site.register(User)

# admin.site.register(User)


# admin.site.unregister(UserPost)
# admin.site.register(UserPost)

# admin.site.register(Post)
admin.site.register(Profile)
# admin.site.register(Friend)

# from .models import User
#
# admin.site.register(User)