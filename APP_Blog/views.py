from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, View, TemplateView
from APP_Blog.models import Blog, Comment, Likes
from APP_Blog.forms import CommentForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid

# def blog_list(request): 
#     return render(request, 'APP_Blog/blog_list.html',context = {})


class MyBlog(TemplateView,LoginRequiredMixin):
    template_name = 'APP_Blog/my_blogs.html'
    

class CreateBlog(LoginRequiredMixin,CreateView):
    # fields = '__all__'
    fields = ('blog_title', 'blog_content','blog_image')
    model = Blog
    template_name = 'APP_Blog/create_blog.html'

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid5)
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
    

    
class Updateblog(LoginRequiredMixin, UpdateView):
    fields = ('blog_title', 'blog_content','blog_image')
    model = Blog
    template_name = 'APP_Blog/edit_blog.html'


    #following function doesn't change the slug
    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('APP_Blog:blog_details', kwargs={'slug':self.object.slug})


    #following function changea the slug
    def form_valid(self, form, **kwargs):
        blog_obj = form.save(commit=False)
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid5)
        blog_obj.save()
        return HttpResponseRedirect(reverse_lazy('APP_Blog:blog_details', kwargs={'slug':self.object.slug}))


    def get_success_url(self, **kwargs):
        return reverse_lazy('APP_Blog:blog_details', kwargs={'slug':self.object.slug})



    
class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'APP_Blog/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')


@login_required
def blog_details(request,slug):

    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('APP_Blog:blog_details', kwargs={'slug':slug}))

    dict ={'blog':blog,
           'comment_form':comment_form,
            'liked' : liked}
    return render(request, 'APP_Blog/blog_details.html',context = dict)


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)     
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog,user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('APP_Blog:blog_details', kwargs={'slug':blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)     
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('APP_Blog:blog_details', kwargs={'slug':blog.slug}))