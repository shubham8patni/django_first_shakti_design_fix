from .models import Post
from django import forms
from django.db import models

from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = ["title", "content"]


class PostFormUpdate(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = ["title", "content"]