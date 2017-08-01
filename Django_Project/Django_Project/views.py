# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
import os
from Demoapp.forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm, CategoryForm, SearchUserForm, UpvoteForm
from Demoapp.models import UserModel, SessionToken, PostModel, LikeModel, CommentModel, CategoryModel, UpvoteModel
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from Django_Project.settings import BASE_DIR
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
#from clarifai import rest
from clarifai.rest import ClarifaiApp
#using clarifai to categorizing Images According To Different Category
import smtplib
#smtplib is used to send email to a particular user who has performed certain actions(like post ,like etc)
from constants import constant, CLARIFAI_API_KEY
from enum import Enum

#all contants are stored in it
import ctypes
import tkMessageBox
from imgurpython import ImgurClient
#(Imgur Saves THe IMage TO cloud using Clent id and client secret)
#client_id = '50b7d2b49057d21'
#client_secret = 'bcfb26bd61078f458bc58d45ad80416c8dc0e6e2'



# Create your views here.
#The signup_view file is created to signup the Instagram Clone using username,name,email,and,password
def signup_view(request) :     #sigup here
    #Business Logic starts here

    if request.method=='GET' :  #IF GET REQUEST IS RECIEVED THEN DISPLAY THE SIGNUP FORM

        form = SignUpForm()

    elif request.method=='POST' :   #for post request
        form = SignUpForm(request.POST)
        if form.is_valid() : #Checks While Valid Entries Is Performed Or Not
            if len(form.cleaned_data['username']) < 4 or len(form.cleaned_data['password']) < 5: #username at least 4 character and password at least 5 characters
                ctypes.windll.user32.MessageBoxW(0, u" Kindly re-enter username or password!min(4)usename and 5 character for password",
                                                 u"INSUFFICIENT CHARACTERS.", 0)

            else :
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                name=form.cleaned_data['name']
                password=form.cleaned_data['password']
                #here above cleaned_data is used so that data could be extracted in safe manner,checks SQL injections
                #following code inserts data into database

                new_user=UserModel(name=name,password=make_password(password),username=username,email=email)
                new_user.save()   #finally saves the data in database


                #sending welcome Email To User That Have Signup Successfully
                message = "Welcome!! To Creating Your Account At p2p marketplace Managed by vikas raj.You Have " \
                      "Successfully Registered.It is correct place for marketing Your product.We Are Happy To Get You" \
                      "as one of our member "
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login('vikasrajuniversity@gmail.com',constant)
                server.sendmail('vikasrajuniversity@gmail.com',email,message)
                #   WOW!!!SUCCESSFULLY SEND EMAIL TO THE USER WHO HAS SIGNUP.USER CAN CHECK INBOX OR SPAM
                # THIS IS ACCURATLY WORKING
                ctypes.windll.user32.MessageBoxW(0, u"You have successfully signed up.",
                                                 u"Congratulations!", 0)
                #(showing message to user for successfully signing up)
                response = redirect('/feed/')
                return response


    return render(request, 'signup.html',{'form': form})



# The login_view function is created to login the Instagram Clone using username and password
def login_view(request) :
    response_data = {}
    if request.method == 'GET' :#display form
        template='login.html'    #it will redirect to login page
        form = LoginForm()       #object


    elif request.method =='POST' :
        form = LoginForm(request.POST)
        if form.is_valid() :             #checks whether entriesd in form is valid or not
            username=form.cleaned_data['username']      #extracting username and password in secure way
            password=form.cleaned_data['password']      #which was entered by user in login form
            #check user exists in database or not
            user=UserModel.objects.filter(username=username).first()    #reads data from database
            #Above SELECT * from user model where username=username
            #This is SQL Querie for above statement

            if user :  #checks whether user exist in database or not
                #comparison of password here
                #comparison sof password here
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
                else:
                    #password is incorrects
                    ctypes.windll.user32.MessageBoxW(0, u"Invalid Password!!!kindly enter correct password", u"Error", 0)
                    response_data['message'] = 'Please try again!'
                    redirect('/login/')
            else:
                ctypes.windll.user32.MessageBoxW(0, u"Invalid Username !!enter valid name", u"Error", 0)
                redirect('/login/')
    response_data['form'] = form
    return render(request,template,{'form':form})


#The feed_view function is created to feed the form after signup an login function Completed
def feed_view(request) :
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

            comments = CommentModel.objects.filter(post_id=post.id)
            #Logic for upvoting
            for comment in comments:
                existing_upvote = UpvoteModel.objects.filter(user=user, comment_id=comment.id).first()
                if existing_upvote:
                    comment.has_upvoted = True

        return render(request, 'feeds.html', {'posts': posts,'comments':comments})
    else:

        return redirect('/login/')

# The check_validation is created for check and maintan validation
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first() #if session has already created on server
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


# The add_category funcrion is created to categories images seprately
def add_category(post):
    app = ClarifaiApp(api_key='{bca96d1642af46ec8c6b9321f53f7cba}')#bb5b6

    # Logo model

    model = app.models.get('general-v1.3')
    response = model.predict_by_url(url=post.image_url)

    if response["status"]["code"] == 10000:
        if response["outputs"]:
            if response["outputs"][0]["data"]:
                if response["outputs"][0]["data"]["concepts"]:
                    for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                        category = CategoryModel(post=post, category_text = response["outputs"][0]["data"]["concepts"][index]["name"])
                        category.save()
                else:
                    print "No concepts list error."
            else:
                print "No data list error."
        else:
            print "No output lists error."
    else:
        print "Response code error."


# The post_view function is created to post an image on Instagram Clone
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

                add_category(post)  #Calling Add category for which furture contact to clarifai
                app = ClarifaiApp(api_key='{bca96d1642af46ec8c6b9321f53f7cba}')
                model = app.models.get('general-v1.3')  # notify model which we are going to use from clarifai
                response = model.predict_by_url(url=post.image_url)  # pass the url of current image
                category = response["outputs"][0]["data"]["concepts"][0][
                    "name"]  # abstarct category name from json response
                post.category = category  # pass value to postModel
                post.save() #save in category field of the POSTMODEL
                ctypes.windll.user32.MessageBoxW(0, u"Your new post is ready.",
                                                 u"Well done!", 0)

                return redirect('/feed/')
            else :
                ctypes.windll.user32.MessageBoxW(0, u"Kindly re-check.",
                                                 u"Ooops!", 0)

        else :
            form = PostForm()
        return render(request, 'posts.html', {'form' : form})

    else :
        return redirect('/login/')

# The search_view function is created to search request and responces
def search_view(request):
    user=check_validation(request)
    if user and request.method=="GET":
        form=SearchUserForm()
        return render(request, 'search.html', {'form': form})
    elif request.method == "POST":
        form = SearchUserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            posts = PostModel.objects.filter(user__username=username)
            return render(request, 'feed.html', {'posts': posts})
    return redirect('/login/')



def search_user_view(request,username):
    posts = PostModel.objects.filter(user__username=username)
    return render(request, 'feed.html', {'posts': posts})



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
                ctypes.windll.user32.MessageBoxW(0, u"Keep scrolling for more.",
                                             u"Liked!", 0)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                to_email = like.post.user.email
                message = "You have a new like on your post posted on instaclone.WEll done keep posting to get more popular"
                server.login('vikasrajuniversity@gmail.com', constant)
                server.sendmail('vikasrajuniversity@gmail.com', to_email, message)

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

            ctypes.windll.user32.MessageBoxW(0, u"Keep scrolling for more.",
                                             u"Successfully Comment added!", 0)
            to_mail = comment.post.user.email
            text_message = "hi!!!you have one new comment on your post.Keep posting To get more comments" \
                           "Thank You TEAM::ACADVIEW"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('vikasrajuniversity@gmail.com', constant)
            server.sendmail('vikasrajuniversity@gmail.com', to_mail, text_message)
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')

#view category_view function  is created to view post of particular category
def category_view(request):
    user = check_validation(request)

    if user and request.method=="GET":
        posts = PostModel.objects.all().order_by('created_on') #pass all images data when categories are to be displayed
        return render(request, 'categories.html', {'posts': posts})
    elif request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            posts = PostModel.objects.filter(category=category) #select only those post which have same category as selected by user
            return render(request, 'feed.html', {'posts': posts})
        else:
            return redirect('/feed/')

    return redirect('/login/')

# the view function is created to comment on instaclone post
def upvote_view(request):
      user = check_validation(request)
      if request.method == 'POST':
          form = UpvoteForm(request.POST)
          if form.is_valid():
              comment_id = form.cleaned_data.get('comment').id
              existing_upvote = UpvoteModel.objects.filter(comment_id=comment_id, user=user).first()
              if not existing_upvote:  # if comment is not upvoted by current user
                  UpvoteModel.objects.create(comment_id=comment_id, user=user)
              else:
                  existing_upvote.delete()  # devote comment
              return redirect('/feed/')
          else:
              return redirect('/login/')
      else:
          return redirect('/login/')
      #return redirect('/index/')

# Ai the end Implemented the logout Funcnality
def logout_view(request):
    request.session.modified = True
    response = redirect("/login/")

    ctypes.windll.user32.MessageBoxW(0, u"You've been logged out successfully!",
                                     u"Thank you!", 0)

    response.delete_cookie(key="session_token")
    return response