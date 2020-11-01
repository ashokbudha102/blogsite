from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ('title','overview','thumbnail','content','categories','featured','previous_post','next_post')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'class': 'form-control', 'name': "usercomment",
                                                           'id': "usercomment", 'placeholder': "Type Comment Here"}))

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name':"username",'id':"username",'placeholder':"Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={
                            'class': 'form-control', 'name': "username", 'id': "useremail", 'placeholder': "Email(optional and will not be published)**"}))
    class Meta:
        model=Comment
        fields=['username','email','content']
