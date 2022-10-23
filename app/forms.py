from socket import fromshare
from django import forms

from app.models import Comment, Subscribe

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'content', 'email', 'name', 'website'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment...'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['website'].widget.attrs['placeholder'] = 'Website (Optional)'


class SubscribeForm(forms.ModelForm):
    """Form definition for Subscribe."""
    class Meta:
        """Meta definition for Subscribeform."""
        model = Subscribe
        fields = '__all__'
        labels = {'email': '',}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email...'
