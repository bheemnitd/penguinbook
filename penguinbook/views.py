from django.shortcuts import render, redirect, HttpResponse
from .form import RegistrationForm, ProfileForm, PostForm, GenderAndDateOfBirthForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from penguinbook.models import Profile, Post, Friend, Message, Like, Comment
from django.contrib.auth.models import User
from datetime import datetime as dt
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.core import serializers
from django.db.models import Q
from django.db.models import F
# import json

# @login_required
@transaction.atomic
def index(request): 
    
    """
    The function is the first page of this app, allow a new user to
    register or an existing user to login. both authentication and aurthorization
    exist in the same page. After authentication the user will be automaticaly loged-in,
    and find himself at homepage of this app. This function is also used for password reset.
    First step is, verify whether the user already registered(authenticated) or not.
    if user is already registered then user will get password reset modal otherwise account
    not found related message will be appeared. 
    """
    
    if request.method == 'POST':
        print("request.POST:",request.POST)

        # CODE FOR LOGIN AFTER SIGNUP.
        if 'signup-form' in request.POST:

            signup_form     = RegistrationForm(request.POST)
            gender_dob_form = GenderAndDateOfBirthForm(request.POST)
            login_form = AuthenticationForm()

            # signup_form = RegistrationForm(request.POST, instance=request.user)
            # profile_form = ProfileForm(request.POST, instance=request.user.profile)

            if signup_form.is_valid() and gender_dob_form.is_valid():
                username = signup_form['username'].data
                password = signup_form['password1'].data
                user = signup_form.save()
                gender_dob_form = gender_dob_form.save(commit=False)
                gender_dob_form.user = user
                gender_dob_form.save()
                username = authenticate(username=username, password=password)
                login(request, username)
                
                Post.objects.create(user_id=user.id, post_text="Penguinbook welcomes you :-)")
                return redirect('home')
                
            # signup_form     = RegistrationForm()
            # gender_dob_form = GenderAndDateOfBirthForm()
            return render(request, 'penguinbook/index.html', {  
                                                                'signup_form': signup_form,
                                                                'gender_dob_form':gender_dob_form,
                                                                'login_form': login_form
                                                                })

        # SCRIPT TO LOGIN.
        elif 'login-form' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            username = authenticate(username=username, password=password)
            if username is not None:
                login(request, username)
                return redirect('home')

            login_form      = AuthenticationForm(request.POST)
            signup_form     = RegistrationForm()
            gender_dob_form = GenderAndDateOfBirthForm()

            login_form.errors['error'] = "Invalid username or password!"
            print("login_form.errors['error']:",login_form.errors['error'])

            return render(request, 'penguinbook/index.html', {
                                                                'signup_form': signup_form,
                                                                'gender_dob_form':gender_dob_form,
                                                                'login_form': login_form
                                                                })
            
        # SCRIPT FOR VERIFYING EMAIL WHETHER USER EXIST OR NOT.
        elif 'find_email' in request.POST:
            try:
                obj = User.objects.get(email=request.POST['find_email'])
                return JsonResponse({'flag':'email exist'})
                
            except Exception as e:
                return JsonResponse({'flag':'email not exist'})

        # SCRIPT FOR RESETTING PASSWORD.
        #elif 'new_password' in request.POST:
            print("else executed.")
            obj = User.objects.get(email=request.POST['email'])
            obj.set_password(request.POST['new_password'])
            obj.save()
            return JsonResponse({'flag':'New password saved successfully.'})

    signup_form = RegistrationForm()
    login_form = AuthenticationForm()
    gender_dob_form=GenderAndDateOfBirthForm()

    return render(request, 'penguinbook/index.html', {  'signup_form': signup_form,
                                                        'login_form': login_form,
                                                        'gender_dob_form':gender_dob_form,
                                                        })
def user_logout(request):   

    logout(request)

    return redirect('index')

@login_required
def home(request):

    if request.method == 'GET':

        # FRIENDS AND PENDING_SENT_FRIEND_REQUEST(FRIEND REQUEST NOT YET ACCEPTED BY OTHER SIDE) OF CURRENT USER .
        mix1_friends = Friend.user.through.objects.filter(user_id=request.user.id).values_list('friend_id',flat=True)

        # FRIENDS OF CURRENT USER.
        friends = Friend.user.through.objects.filter(user_id__in=mix1_friends, friend_id=request.user.id).values_list('user_id',flat=True)

        # PENDING_SENT_FRIEND_REQUEST(FRIEND REQUEST NOT YET ACCEPTED BY OTHER SIDE) OF CURRENT USER
        pending_sent_friend_request = User.objects.filter(id__in=list(set(mix1_friends)-(set(friends))))
                 
        # FRIENDS AND PENDING_RECEIVED_FRIEND_REQUEST OF CURRENT USER.(FRIEND REQUEST NOT YET ACCEPTED BY CURRENT USER.)
        mix2_friends = Friend.user.through.objects.filter(friend_id=request.user.id).values_list('user_id',flat=True)

        # PENDING_SENT_FRIEND_REQUEST(FRIEND REQUEST NOT YET ACCEPTED BY OTHER SIDE) OF CURRENT USER
        pending_received_friend_request = User.objects.filter(id__in=list(set(mix2_friends)-(set(friends))))

        unknown_avatars = User.objects.exclude(id__in=friends).exclude(id=request.user.id)

        friends_post=Post.objects.exclude(user_id__in=unknown_avatars.values('id')).order_by('-id')
        
        friends = User.objects.filter(id__in=friends)
        # SORT THE FRIENDS_POST ORDER BY POST_DATE SO WE CAN GET LATEST POST ON TOP.            
        # friends_post.sort(key=lambda r: r.post_date, reverse=True)
        
        # post = Post.objects.filter(user_id=18)
        # for p in post:
        #     likes = Like.objects.filter(post_id=p.id)
            # print("like of ",p,"is ",likes)
            # print("likes:",likes)
        friend_post = list()
        for post in friends_post:
            friend_post.append({'post':post,
                                'likes':User.objects.filter(id__in=Like.objects.filter(post_id=post.id).values('user_id')),
                                'comments':Comment.objects.filter(post_id=post.id).order_by("-comment_time").values('comment_text','user__first_name','user__last_name')
                                })
        
        # likes = Like.objects.filter(post_id__in=friends_post.values('id'))
        # for like in likes:
        #     print("liked:",like.post_id)
        #     break
        post_form = PostForm()
        return render(request, 'penguinbook/home.html', {'post_form'   :post_form,
                                                        #   'public_post' :public_post,
                                                        
                                                        'friends_post':friend_post,
                                                        'friends':friends,
                                                        'pending_received_friend_request':pending_received_friend_request,
                                                        'unknown_avatars':unknown_avatars, #PUBLIC PROFILES WHICH IS NOT FRIEND OF CURRENT USER.
                                                        'pending_sent_friend_request':pending_sent_friend_request,
                                                        
                                                        })
    # post_form=PostForm(request.POST, request.FILES)
    print('request.POST:', request.POST)               
    print('request.FILES:', request.FILES)

    if 'post_image' in request.FILES:
        cropper_x = float(request.POST['cropper_x'])
        cropper_y = float(request.POST['cropper_y'])
        cropper_height = float(request.POST['cropper_height'])
        cropper_width = float(request.POST['cropper_width'])
        
        image = Image.open(request.FILES['post_image'])
        cropped_image = image.crop((cropper_x, cropper_y, cropper_width+cropper_x, cropper_height+cropper_y))

        Post.objects.create(user_id=request.user.id, post_image=request.FILES['post_image'], post_text=request.POST['about_post'])
        instance = Post.objects.filter(user_id=request.user.id).order_by('-post_date')[0]
        
        cropped_image.save(instance.post_image.path)
        instance.post_text=request.POST['about_post']
        instance.save()
        return redirect('home')
    elif 'message_receiver_id' in request.POST:

        chat_history = serializers.serialize('json', Message.objects.filter(Q(user_id=request.user.id, message_receiver_id=request.POST['message_receiver_id'])|Q(user_id=request.POST['message_receiver_id'], message_receiver_id=request.user.id)).order_by('id'))
        # for message in chat_history:
        #     print(message.message)
        # chat_history = serializers.serialize('json', list(chat_history))
        print("rturning multiple time.")
        return JsonResponse(chat_history, safe=False)
    elif 'post_text' in request.POST:
        Post.objects.create(user_id=request.user.id, post_text=request.POST['post_text'])
        return JsonResponse({'flag':request.POST['post_text']})

    elif 'like_status' in request.POST:

        # if 'liked' == request.POST['like_status']:
        like_status = Like.objects.filter(post_id=request.POST['post_id'], user_id=request.user.id)
        if like_status:
            like_status.delete()
        else:
            Like.objects.create(user_id=request.user.id, 
                                post_id=request.POST['post_id'], 
                                like_gainer_id=request.POST['like_gainer_id'], 
                                like_status=request.POST['like_status'])
                                
            # Post.objects.filter(id=request.POST['post_id']).update(likes=F('likes')+1)
            # Post.objects.filter(id=request.POST['post_id']).update(likes=F('likes')-1)

        #     print("working")

        # # likes_of_post=Post.objects.get(id=request.POST['post_id']).likes
        # likes_of_post = Like.objects.filter(post_id=request.POST['post_id']).count()
        # Post.objects.filter(id=request.POST['post_id']).update(likes=likes_of_post)
        return JsonResponse({'update':'success'})
    elif 'comment_text' in request.POST:
        Comment.objects.create( post_id=request.POST['post_id'],
                                user_id=request.POST['commenter_id'],
                                comment_gainer_id=request.POST['poster_id'],
                                comment_text=request.POST['comment_text'])
        comments_of_post=Comment.objects.filter(post_id=request.POST['post_id'])

        # comments_of_post = serializers.serialize('json', comments_of_post)
        # return HttpResponse(data, content_type="application/json")

        return JsonResponse({'new_comment':request.POST['comment_text'],
                            'first_name':request.user.first_name,
                            'last_name':request.user.last_name
                            })
    # return render(request)

@login_required
def profile(request):
    
    id = list(request.GET.keys())[0]
    # FRIENDS AND PENDING_RECEIVED_FRIEND_REQUEST OF CURRENT USER.(FRIEND REQUEST NOT YET ACCEPTED BY CURRENT USER.)
    mix_friends = Friend.user.through.objects.filter(friend_id=request.user.id).values_list('user_id',flat=True)
    
    # FRIENDS OF CURRENT USER.
    friends = Friend.user.through.objects.filter(user_id=request.user.id, friend_id__in=mix_friends).values_list('friend_id',flat=True)

    # PENDING_SENT_FRIEND_REQUEST(FRIEND REQUEST NOT YET ACCEPTED BY OTHER SIDE) OF CURRENT USER
    pending_received_friend_request = User.objects.filter(id__in=list(set(mix_friends)-(set(friends))))
    print(len(pending_received_friend_request))
    friends = User.objects.filter(id__in=friends)

    # CODE TO OPEN PROFILE OF A AVATAR.
    avatar = User.objects.get(id=list(request.GET.keys())[0])
    if request.method == 'GET':

        id = list(request.GET.keys())[0]
        timeline=Post.objects.filter(user_id=id).order_by('-post_date')

        print("profile.id:", avatar.id)
        print("request.user.id", request.user.id)
        print('profile:', avatar.profile.gender)

        if avatar.id in Friend.user.through.objects.filter(user_id=request.user.id).values_list('friend_id', flat=True):
    
            if request.user.id in Friend.user.through.objects.filter(user_id=avatar.id).values_list('friend_id', flat=True):
            
                avatar.profile.friendship_status = 'Friend'
            else:
                avatar.profile.friendship_status = 'Cancel Request'                    

        elif request.user.id in Friend.user.through.objects.filter(user_id=avatar.id).values_list('friend_id', flat=True):

                avatar.profile.friendship_status = 'Accept Request'
                # avatar.profile.number_of_friend_request_to_accept=Friend.user.through.objects.filter(user_id=avatar.id).values_list('friend_id', flat=True).count()
                # print('number_of_friend_request_to_accept',profile['number_of_friend_request_to_accept'])
        else:
            avatar.profile.friendship_status = 'Add Friend'

        profile_form = ProfileForm()
        return render(request, 'penguinbook/profile.html', {'profile_form' : profile_form,
                                                            'avatar': avatar,
                                                            'friends':friends,
                                                            'pending_received_friend_request':pending_received_friend_request,
                                                            'timeline':timeline,
                                                           })
        
    # SCRIPT TO SAVE THE RECORD OF FRIEND REQUEST SENDER TO DATABASE
    print("request.POST:", request.POST)
    if 'action' in request.POST.keys():
        print(request.POST['id'])
        print(request.POST['action'])
        friend = Friend(id=request.POST['id'])

        if request.POST['action'] == "Add Friend":

            friend.save()
            friend.user.add(User.objects.get(id=request.user.id))
            return JsonResponse({'friendship_status':'Cancel Request'})
            
        elif request.POST['action'] == "Accept Request":

            friend.save()
            friend.user.add(User.objects.get(id=request.user.id))
            return JsonResponse({'friendship_status':'Friend'})

        elif request.POST['action'] == "Cancel Request":

            friend.user.remove(User.objects.get(id=request.user.id))
            return JsonResponse({'friendship_status':'Add Friend'})
        else:
            return JsonResponse({'friendship_status':'Friend'})
    # print('request.FILES:', request.FILES)
    # print("request.POST:", request.POST)
    
    # print("request.POST['photo_upload_flag']",request.POST['photo_upload_flag'])
    cropper_x = float(request.POST['cropper_x'])
    cropper_y = float(request.POST['cropper_y'])
    cropper_height = float(request.POST['cropper_height'])
    cropper_width = float(request.POST['cropper_width'])
    # about_post = request.POST['about_post']

    if 'input-display-picture' == request.POST['photo_upload_flag']:

        user = User.objects.get(id=request.user.id)
        user.profile.display_picture=request.FILES['display_picture']
        user.save()

        image = Image.open(request.FILES['display_picture'])
        cropped_image = image.crop((cropper_x, cropper_y, cropper_width+cropper_x, cropper_height+cropper_y))
        if cropper_width<200:
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(user.profile.display_picture.path)
        else:
            cropped_image.save(user.profile.display_picture.path)

        Post.objects.create(user_id=request.user.id, post_text=request.POST['about_post'])
        instance = Post.objects.filter(user_id=request.user.id).order_by('-post_date')[0]
        instance.post_image=user.profile.display_picture
        instance.save()

    else:   

        user = User.objects.get(id=request.user.id)
        user.profile.display_cover=request.FILES['display_cover']
        user.save()

        image = Image.open(request.FILES['display_cover'])
        cropped_image = image.crop((cropper_x, cropper_y, cropper_width+cropper_x, cropper_height+cropper_y))
        if cropper_width<900:
            resized_image = cropped_image.resize((900, 300), Image.ANTIALIAS)
            resized_image.save(user.profile.display_cover.path)
        else:
            cropped_image.save(user.profile.display_cover.path)


        Post.objects.create(user_id=request.user.id, post_text=request.POST['about_post'])
        instance = Post.objects.filter(user_id=request.user.id).order_by('-post_date')[0]
        instance.post_image=user.profile.display_cover
        instance.save()

    profile = dict()
    id = list(request.GET.keys())[0]
    profile['display_picture']  = Profile.objects.filter(user_id=id).exclude(display_picture='').last()
    profile['display_cover']    = Profile.objects.filter(user_id=id).exclude(display_cover='').last()
    profile['user']             = User.objects.get(id=id)
    profile_form = ProfileForm()
    return render(request, 'penguinbook/profile.html',{'profile_form' : profile_form,
                                                       'avatar': avatar,
                                                       'friend_request_to_be_accepted':pending_received_friend_request,
                                                    })
def password_reset(request):

    # obj = User.objects.filter(email=request.POST['email'])
    print('PASSWORD RESET CALLED.')
    return render(request, 'penguinbook/index.html')
    # user_profile_form = ProfileForm()
    # return HttpResponse("{'action': 'success'}")

# def friends_profile(request):

#     profile_image_obj = UserProfile.objects.filter(author_id=request.user.id).exclude(profile_image='').last()
#     # profile_image_obj = UserProfile.objects.filter(author_id=request.user.id, profile_image__isnull=False).last()
#     profile_cover_obj = UserProfile.objects.filter(author_id=request.user.id).exclude(profile_cover='').last()
#     return render(request, 'penguinbook/profile.html', {
#                                                      'profile_image_obj': profile_image_obj,
#                                                      'profile_cover_obj': profile_cover_obj})
# def display(request):
#     user_profile_form = UserProfileForm()
#     return render(request, 'penguinbook/display.html', {'user_profile_form': user_profile_form})