#coding:utf-8
#blog>forms.py
from django import forms

from .models import Post,Comment

#投稿用フォーム
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','text',)

#コメント用フォーム
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)