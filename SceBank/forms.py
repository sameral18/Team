import profile

from django.contrib.auth import get_user_model
from django import forms
from .models import User

class SignupForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'website', 'picture')

    def save(self, user):
        profile.save()
        user.save()