# _*_ coding: utf-8 _*_

from __future__ import unicode_literals
from django.shortcuts import render
from datetime import datetime
#create your views here.
def signup_view(request):
	#business Logic.
	today = datetime.now
	return render(request, 'signup.html', {'today':today})

