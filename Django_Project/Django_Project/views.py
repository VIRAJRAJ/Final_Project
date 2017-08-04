# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
import os
from Demoapp.forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from Demoapp.models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from Django_Project.settings import BASE_DIR
from django.contrib.auth.hashers import make_password,check_password
#from clarifai import rest
from clarifai.rest import ClarifaiApp

from constants import constant, CLARIFAI_API_KEY
from imgurpython import ImgurClient
client_id = '50b7d2b49057d21'
client_secret = 'bcfb26bd61078f458bc58d45ad80416c8dc0e6e2'


def signup_view(request) :     
    #Business Logic starts here

    if request.method=='GET' : 

        form = SignUpForm()

    elif request.method=='POST' :
        form = SignUpForm(request.POST)
        if form.is_valid() : 
    

   
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                name=form.cleaned_data['name']
                password=form.cleaned_data['password']
   

                new_user=UserModel(name=name,password=make_password(password),username=username,email=email)
                new_user.save()   
                response = redirect('/feed/')
                return response


    return render(request, 'signup.html',{'form': form})

def login_view(request) :
    response_data = {}
    if request.method == 'GET' 
        template='login.html'    
        form = LoginForm()      


    elif request.method =='POST' :
        form = LoginForm(request.POST)
        if form.is_valid() :             
            username=form.cleaned_data['username']      
            password=form.cleaned_data['password']      
            #check user exists in database or not
            user=UserModel.objects.filter(username=username).first()    
            
            if user :  
                
                if check_password(password,user.password) :
                    #login successful here

                    new_token = SessionToken(user=user)
                    new_token.create_token()
                    new_token.save()
                    #response = redirect('feed/')
                    response=redirect('/feed/')
                    response.set_cookie(key='session_token', value = new_token.session_token)
                    #template = 'login_success.html'
                    return response
                    #return render(request,template,{'form':form},response)
                    else :
                        response_data['message'] = 'Please try again!'
                        redirect('/login/')
      
    response_data['form'] = form
    return render(request,template,{'form':form})



def feed_view(request) :
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

            comments = CommentModel.objects.filter(post_id=post.id)

        return render(request, 'feeds.html', {'posts': posts,'comments':comments})
    else:

        return redirect('/login/')

# The check_validation is created for check and maintan validation
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None



def post_view(request) :
    user = check_validation(request)

    if user :
        if request.method == 'POST' :
            form = PostForm(request.POST, request.FILES)
            if form.is_valid() :
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR +"//"+ post.image.url)
                #Logic for cloud storage of image
                client = ImgurClient('50b7d2b49057d21', 'bcfb26bd61078f458bc58d45ad80416c8dc0e6e2')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

       
                return redirect('/feed/')
      
            

        else :
            form = PostForm()
        return render(request, 'posts.html', {'form' : form})

    else :
        return redirect('/login/')


def search_user_view(request,username):
    posts = PostModel.objects.filter(user__username=username)
    return render(request, 'feeds.html', {'posts': posts})



#The like_view function is created to like a user post
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                like = LikeModel.objects.create(post_id=post_id, user=user)
                

            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')

# The comment_view function is created to comment on a particular user post
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()

            
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')

              
