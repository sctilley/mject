from .models import CustomUser
from django import forms
from django.contrib.auth.models import User
from .models import Profile


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

#for the admin
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password1',
            'password2'
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'mtgoUserName',
        ]