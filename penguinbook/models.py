from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime as dt
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# class UserRegistration(models.Model):
#
#     first_name = models.CharField(max_length=120)
#     last_name = models.CharField(max_length=120)
#     username = models.CharField(max_length=120,primary_key=True)
#     email = models.EmailField(max_length=120,unique=True, null=False)
#     password = models.CharField(max_length=120)
#     USERNAME_FIELD = 'username'

def display_picture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = filename[:-4]+str(dt.now())+filename[-4:]
    return 'user_{0}/display_picture/{1}'.format(instance.user.id, filename)

def display_cover_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = filename[:-4]+str(dt.now())+filename[-4:]
    return 'user_{0}/display_cover/{1}'.format(instance.user.id, filename)

def post_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = filename[:-4]+str(dt.now())+filename[-4:]
    return 'user_{0}/post_image/{1}'.format(instance.user.id, filename)
GENDER_CHOICES = ( 
("M", "Male"),
("F", "Female"),
("C", "Custom"),) 
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_picture = models.ImageField(upload_to=display_picture_directory_path, null=True)
    display_cover = models.ImageField(upload_to=display_cover_directory_path, null=True)
    display_quotes = models.CharField(max_length=500, blank=True, null = True)
    profile_update_date = models.TimeField(auto_now=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
    secondary_school_name = models.CharField(null=True, max_length=500)
    secondary_school_passing_year = models.DateField(null=True)
    heigher_secondary_school_name = models.CharField(null=True, max_length=500)
    heigher_secondary_school_passing_year = models.DateField(null=True)
    under_graduate_collage_name = models.CharField(null=True, max_length=500)
    under_graduate_collage_passing_year = models.DateField(null=True)
    post_graduate_collage_name = models.CharField(null=True, max_length=500)
    post_graduate_passing_year = models.DateField(null=True)
    doctor_of_philosophy_collage_name = models.CharField(null=True, max_length=500)
    doctor_of_philosophy_collage_passing_year = models.DateField(null=True)
    previous_job =  models.CharField(null=True, max_length=500)
    current_job = models.CharField(null=True, max_length=500)
    native_place = models.CharField(null=True, max_length=500)
    current_living_place = models.CharField(null=True, max_length=500)
    friendship_status = models.CharField(max_length=20,default="Add Friend")
    number_of_friend_request_to_accept = models.IntegerField(default=0)
    # friendship_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Friend(models.Model):
    
    user = models.ManyToManyField(User, related_name='friends')
    friendship_status = models.SmallIntegerField(default=0)
    friendship_date = models.DateField(auto_now=True)
    friendship_appraoch = models.CharField(null=True, max_length=15)

    def __str__(self):
        return self.user.username

class Post(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    # comment = models.ForeignKey(Comment,on_delete=models.CASCADE, null=True)
    # like    = models.ForeignKey(Like,   on_delete=models.CASCADE, null=True)

    post_text  = models.TextField(max_length=5000, blank=True)
    post_image = models.ImageField(upload_to=post_image_directory_path, blank=True, max_length=1000)
    post_date  = models.DateTimeField(auto_now=True)
    # likes = models.SmallIntegerField(default=0)


    # def __str__(self):
    #     return self.user.username
    

    # def __str__(self):
    #     return self.author.author  

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    like_status = models.CharField(null=True, max_length=10)
    like_time = models.DateTimeField(default=timezone.now, db_index=True)
    like_gainer_id = models.SmallIntegerField(null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post,  on_delete=models.CASCADE, null=True)
    # like = models.ForeignKey(Like, related_name='post_likes', on_delete=models.CASCADE, null=True)
    comment_text = models.TextField(max_length=100000, null=True)
    comment_gainer_id = models.SmallIntegerField(null=True)
    comment_time = models.DateTimeField(default=timezone.now, db_index=True)
# class Share(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     post = models.ForeignKey(Post,  on_delete=models.CASCADE, null=True)
#     share_gainer_id=models.SmallIntegerField(null=True)
#     share_time = models.DateTimeField(default=timezone.now, db_index=True)

class Message(models.Model):

    user = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE, null=True)
    message_receiver_id = models.SmallIntegerField(null=True)
    message = models.TextField(max_length=100000, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    # friend = models.prime

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]
# "<frozen importlib._bootstrap>"
# class Room(models.Model):
#     name = models.TextField(max_length=1000)
#     label = models.SlugField(unique=True)

# class UserQuery(models.Model):
#
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     query = models.CharField(max_length=100)

# class UserProfile(models.Model):
#
#     profile_img = models.OneToOneField(User, upload_to='profile_image_path',blank=True)


# <!--    {% for obj in all_post_of_user %}-->
# <!--      <div class="container">-->
# <!--          <h2>User post</h2>-->
# <!--          <div class="well well-lg">-->
#
# <!--              {{obj.post_text}}-->
# <!--              {{obj.post_date}}-->
#
# <!--          </div>-->
# <!--      </div>-->
# <!--    {% endfor %}-->


# try:

#             friend_request_id = Friend.user.through.objects.get(user_id=request.user.id).friend_id
#             print('executing:',request.user.id)

#             try:

#                 if(friend_request_id==profile['user'].id):

#                     profile['friendship_status']= Friend.objects.get(id=friend_request_id).friendship_status

#                 else:

#                     profile['friendship_satatus'] = None

#             except Exception as e:

#                 profile['friendship_satatus'] = None
#                 print('Internal Exception:',e)

#         except Exception as e:

#             profile['friendship_satatus'] = None
#             print('External Exception:', e)