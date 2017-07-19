# _*_ coding: utf-8 _*_

from __future__ import unicode_literals
from django.shortcuts import render
from datetime import datetime
from Demoapp.forms import SignUpForm,LoginForm
from django.contrib.auth.hashers import make_password,check_password
from Demoapp.models import UserModel
#create your views here.
def signup_view(request):
	#business Logic.
	if request.method == 'GET':
		#Display signup form
                #today = datetime.now
		form = SignUpForm()
		template_name = 'signup.html'
	elif request.method == 'POST':
		form = SignUpForm(request.POST)
        if form.is_valid():
		   username = form.cleaned_data['username']
		   email = form.cleaned_data['email']
		   name = form.cleaned_data['name']
		   password = form.cleaned_data['password']
		   # insert data to db
		   new_user = UserModel(name=name, password=make_password(password), username=username, email=email)
		   new_user.save()
		   template_name = 'success.html'

                   
        return render(request, template_name, {'form':form})

def login_view(request):
	if request.method == 'GET':
		# to do Display login form
		template_name = 'login.html'
		form = LoginForm()
	elif request.method == 'POST':
		# to do : process form data
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			#chech user exist in db or not
			user = UserModel.objects.filter(username=username).first()
			if user:
			        #compare password
				if check_password(password, user.password):
				     #login successful
				     template_name = 'login_success.html'
				else:
			             # password  is incorrect.
				     template_namew = 'login_fail.html'
	                else:
				 template_name = 'login_fail.html'
       
        return render(request,template_name,{'form' : form})

