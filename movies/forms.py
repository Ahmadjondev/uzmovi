from django import forms
from .models import Comment, Rating

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        fields = ['content', 'parent_id']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your comment...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.Select(attrs={'class': 'form-select'}),
        }
