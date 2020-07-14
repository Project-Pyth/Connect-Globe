from django import forms
from MyApp.models import Post



class CreatePostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ['title', 'body']





