from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import  UserCreationForm
import datetime

User = get_user_model()

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField(Label="Email", max_length=300)
    dob = forms.DateField(label="Date of Birth (mm dd yyyy)", required=True,
                          initial=datetime.date.today, widget=forms.DateInput())

    class Meta:
        model = User
        fields = ["username", "email", "dob", "password"]

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
         # fields = ("email", "password")
        fields = ("username", "password")

    def clean(self):
        if self.is_valid():
            username = self.clened_data["Username"]
            password = self.cleaned_data["Password"]
            # if not authenticate(email=email, password=password):
            #     raise forms.ValidationError(f"Wrong password or email")
            # return self.cleaned_data
            if not authenticate(password=password, username=username):
                raise forms.ValidationError(f"Wrong password or username")
        return self.cleaned_data


