from django.urls import path
from penguinbook import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    # path('', views.password_reset, name='password_reset')
    # path('friends_profile/', views.friends_profile, name='friends_profile'),
    # path('display/', views.display, name = 'display'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)