from django import forms
from .models import Comment


class ImageUploadForm(forms.Form):
    name = forms.CharField(max_length=200)
    image = forms.ImageField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SearchForm(forms.Form):
    search = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter keywords to search products: white cat'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ApiQuestionForm(forms.Form):
    user = forms.IntegerField()
    title = forms.CharField(max_length=200)
    body = forms.Textarea()
