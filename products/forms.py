from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'دیدگاه شما'}))

    class Meta:
        model = Comment
        fields = ('description',)


class CommentReplyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پاسخ شما'}))

    class Meta:
        model = Comment
        fields = ('description',)        