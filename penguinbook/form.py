from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from penguinbook.models import Profile, Post 
from django import forms
from PIL import Image

# class Meta:
#     model = User
#     fields = ("username",)

class RegistrationForm(UserCreationForm):

    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

class PostForm(ModelForm):
    cropper_x = forms.FloatField(widget=forms.HiddenInput())
    cropper_y = forms.FloatField(widget=forms.HiddenInput())
    cropper_height = forms.FloatField(widget=forms.HiddenInput())
    cropper_width = forms.FloatField(widget=forms.HiddenInput())
    about_post=forms.CharField(widget=forms.HiddenInput())
    class Meta:

        model = Post
        fields = (  'post_text',
                    'post_image',
                    'cropper_x',
                    'cropper_y',
                    'cropper_height',
                    'cropper_width',
                    'about_post'
                    )
        # widgets = {
        #     'post_text': Textarea(attrs={'row': 2, 'style': 'width: 100%'}),
        # }

# class ProfileUpdateForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('display_picture', 'display_cover', 'display_quotes',
#         'date_of_birth', 
#         'secondary_school_name',
#         'secondary_school_passing_year',
#         'heigher_secondary_school_name',
#         'heigher_secondary_school_passing_year', 
#         'under_graduate_collage_name', 
#         'under_graduate_collage_passing_year',
#         'post_graduate_collage_name', 
#         'post_graduate_passing_year',
#         'doctor_of_philosophy_collage_name',
#         'doctor_of_philosophy_collage_passing_year',
#         'previous_job',
#         'current_job',
#         'native_place',
#         'current_living_place',
#         )
class GenderAndDateOfBirthForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'gender',)

class ProfileForm(ModelForm):

    cropper_x = forms.FloatField(widget=forms.HiddenInput())
    cropper_y = forms.FloatField(widget=forms.HiddenInput())
    cropper_height = forms.FloatField(widget=forms.HiddenInput())
    cropper_width = forms.FloatField(widget=forms.HiddenInput())
    photo_upload_flag = forms.CharField(widget=forms.HiddenInput())
    about_post = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = (  'display_cover', 
                    'display_picture', 
                    'cropper_x', 
                    'cropper_y', 
                    'cropper_height', 
                    'cropper_width', 
                    'photo_upload_flag', 
                    'about_post',
                    )
        
# class UserQueryForm(UserCreationForm):
#
#     class Meta:
#
#         model = UserQuery
#
#         fields = ('query',)
# class UserLoginForm(models.Model):
#
#     pass
#
#
