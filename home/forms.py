from django import forms
from .models import Comment


class ImageUploadForm(forms.Form):
    name = forms.CharField(max_length=200)
    image = forms.ImageField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']