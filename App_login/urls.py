from django.urls import path
from App_login import views

app_name = 'App_login'
urlpatterns = [
     path('signup/',views.sign_up,name='Signup'), 
     path('login/',views.login_page,name='Login'),
     path('logout/',views.user_logout,name='Logout'),
     path('profile/',views.profile_page,name='Profile'),
     path('change-profile/',views.Userprofile_change,name='user_change'),
     path('password/', views.pass_change, name='pass_change'),
     path('add-picture/', views.add_pro_pic, name='add_pro_pic'),
     path('change-picture/', views. change_pro_pic, name='change_pro_pic'),

]

