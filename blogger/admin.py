from django.contrib import admin
# from django.db import models
from .models import Post, Upload
from tinymce.widgets import TinyMCE
from django import forms

class PostFormAdmin(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = ["title", "content", "date_posted", "author"]
        

class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin

admin.site.register(Post, PostAdmin)

admin.site.register(Upload)