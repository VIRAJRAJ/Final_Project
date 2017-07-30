# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#from clarifai.rest import ClarifaiApp
#from clarifai.rest import Image as ClImage
#app = ClarifaiApp(api_key = '{bca96d1642af46ec8c6b9321f53f7cba}')
#get the general model
model = app.models.get("general-v1.3")
# make an image with an url
img = ClImage(url='https://samples.clarifai.com/dog1.jpeg')
model = app.models.get('puppy')
model.predict_by_url('https://samples.clarifai.com/metro-north.jpg')
