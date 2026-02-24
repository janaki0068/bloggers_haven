
from django import forms
from .models import Article, Comment , Profile # if you have these models

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us a little about yourself…',
                'rows': 3,
                'cols': 40,
            })
        }