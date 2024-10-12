from django.urls import path
from APP_Blog import views

app_name = 'APP_Blog'
urlpatterns = [
    # path('',views.blog_list,name='blog_list'),
    path('',views.BlogList.as_view(),name='blog_list'),
    path('write/',views.CreateBlog.as_view(),name='create_blog'),
    path('details/<slug>/',views.blog_details,name='blog_details'),
    path('liked/<pk>/',views.liked,name='liked_post'),  
    path('unliked/<pk>/',views.unliked,name='unliked_post'),
    path('my-blogs/',views.MyBlog.as_view(),name='my_blogs'), 
    path('edit/<pk>/',views.Updateblog.as_view(),name='edit_blog'),      
]
