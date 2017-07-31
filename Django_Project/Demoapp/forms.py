from django import forms
from models import UserModel,SessionToken,PostModel,LikeModel,CommentModel,UpvoteModel


class SignUpForm(forms.ModelForm) :
    class Meta :
        model = UserModel
        fields = ['email','username','name','password']


class LoginForm(forms.ModelForm) :
    class Meta :
        model = UserModel
        fields = ['username','password']

class PostForm(forms.ModelForm) :
    class Meta :
        model = PostModel
        fields = ['image' , 'caption']


class LikeForm(forms.ModelForm) :

    class Meta :
        model = LikeModel
        fields = ['post']

class CommentForm(forms.ModelForm) :

    class Meta :
        model = CommentModel
        fields = ['comment_text' , 'post' ]

class SearchUserForm(forms.ModelForm) :
    class Meta :
        model = UserModel
        fields = ['username']

class CategoryForm(forms.ModelForm) :
    class Meta :
        model = PostModel
        fields = ['category']

class UpvoteForm(forms.ModelForm) :
    class Meta :
        model = UpvoteModel
        fields = ['comment']
































# from django import forms
# from models import UserModel, SessionToken, PostModel, CommentModel, LikeModel
#
# class SignUpForm(forms.ModelForm):
# 	class Meta:
# 		model = UserModel
# 		fields = ['email','username','name', 'password']
#
# class LoginForm(forms.ModelForm):
# 	class Meta:
# 		model = UserModel
# 		fields = ['username','password']
#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = PostModel
#         fields=['image', 'caption']
#
# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = LikeModel
#         fields=['post']
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = CommentModel
#         fields = ['comment_text', 'post']
#


