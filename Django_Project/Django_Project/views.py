# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from datetime import datetime
from Demoapp1.forms import SignUpForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
from Demoapp1.models import UserModel

# Create your views here.
def signup_view(request):
    if request.method == 'GET':
        #display signup form
        signup_form = SignUpForm()
        template_name = 'signup.html'
    elif request.method == 'POST':
        #process the form data
        signup_form = SignUpForm(request.POST)
        #validate the form data
        if signup_form.is_valid():
            #validation successful
            username = signup_form.cleaned_data['username']
            name = signup_form.cleaned_data['name']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            #save data to db
            new_user = UserModel(name=name, email=email, password=make_password(password), username=username)
            new_user.save()
            template_name = 'success.html'

    return render(request, template_name, {'signup_form':signup_form})

def login_view(request):
    if request.method == 'GET':
        #display login form
        login_form = LoginForm()
        template_name = 'login.html'
    elif request.method == 'POST':
        #process the form data
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #validation successful
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            #read data from db
            user = UserModel.objects.filter(username=username).first()
            if user:
                #compare the password
                if check_password(password, user.password):
                    #login successful
                    template_name = 'login_success.html'
                else:
                    #login failed.
                    template_name = 'login_fail.html'
            else:
                #user does not exist in db.
                template_name = 'login_fail.html'
        else:
            #validation failed
            template_name = 'login_fail.html'

    return render(request, template_name, {'login_form':login_form})