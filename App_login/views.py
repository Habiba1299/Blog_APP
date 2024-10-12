from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from App_login.forms import SignUpForm, UserProfileChange, ProfilePic


def sign_up(request):  
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
        
    dict = {
        'form' : form,
        'registered': registered,
    }

    return render(request, 'App_login/signup.html',context=dict)

def login_page(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form =  AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    return render(request,'App_login/login.html',context={'form':form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile_page(request): 
    return render(request,'App_login/profile.html',context={})

@login_required
def Userprofile_change(request): 
    current_user = request.user
    form = UserProfileChange(instance= current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST,instance= current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance= current_user)
    return render(request,'App_login/change_profile.html',context={'form':form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'App_Login/pass_change.html', context={'form':form, 'changed':changed})


@login_required
def add_pro_pic(request): 
    form = ProfilePic()

    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False) #The pic is collected but it is not submitted in database
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_login:Profile'))

    return render(request,'App_login/pro_pic_add.html',context={'form':form})

@login_required
def change_pro_pic(request): 
    form = ProfilePic(instance=request.user.user_profile)

    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect(reverse('App_login:Profile'))

    return render(request,'App_login/pro_pic_add.html',context={'form':form})

