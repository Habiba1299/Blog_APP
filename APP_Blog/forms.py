from django import forms
from APP_Blog.models import Blog, Comment, Likes


class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ('comment',)
