from django.shortcuts import render,HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Blog_post
import time

# Create your views here.

def home(request):
    posts=Blog_post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def about(request):
    return render(request,'blog/about.html')


def contact(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            name=request.POST['name']
            email=request.POST['email']
            subject=request.POST['subject']
            message=request.POST['message']
            if name and email and subject and message:
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request,'All fields required.')
    return render(request,'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts=Blog_post.objects.all()
        full_name=request.user.get_full_name()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name})
    else:
        return HttpResponseRedirect('/login')
   

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



#USER LOGIN AND AUTHENTICATION SYSTEM
def user_login(request):
    if not request.user.is_authenticated:
        # print("not authenticated")
        if request.method=="POST":
            # print("yes post")
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)

                if user is not None:
                    login(request,user)
                    request.is_authenticated=True
                    messages.success(request,"Logged in successfully.")
                    # time.sleep(1)
                    return HttpResponseRedirect('/dashboard')
            else:
                print("Not valid")
        else:
            print("No post")
        form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard')



#USER SIGN UP PROCESS 
def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! You can now create and post your own blogs')
            form.save()
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})


def add_post(request):
    if request.user.is_authenticated:
        form=PostForm()
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                description=form.cleaned_data['description']
                p=Blog_post(title=title,description=description)
                p.save()
                return HttpResponseRedirect('/dashboard')
            else:
                form=PostForm()
        return render(request,'blog/add_post.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        pid=Blog_post.objects.get(pk=id)
        form=PostForm(instance=pid)
        if request.method=="POST":
            form=PostForm(request.POST,instance=pid)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard')

        return render(request,'blog/update_post.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pid=Blog_post.objects.get(pk=id)
            pid.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
