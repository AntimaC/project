from django import forms
from django.db.models import fields
from django.forms import widgets
from numpy import number
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from .models import  Post,Replie
       

class DashboardFom(forms.Form):
    text=forms.CharField(max_length=100,label="Enter your search:") 
  
class PostContent(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['post_content']
        widgets={
            'post_content':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        
class ReplyContent(forms.ModelForm):
    class Meta:
        model = Replie
        fields = ['reply_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'post_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':10, 'cols':3}),
        }

class UpdateReplyForm(forms.ModelForm):
    class Meta:
        model = Replie
        fields = [ 'reply_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':10, 'cols':3}),
        }