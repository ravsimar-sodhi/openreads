from django import forms
# from Users.models import User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from Users.models import *


class AddShelfForm(forms.Form):
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AddShelfForm, self).__init__(*args, **kwargs)
    name = forms.CharField(label="Add Shelf",min_length=4, max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Shelf Name'}))
    class Meta:
        model = Bookshelf

        fields = (
            'name'
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            shelf = Bookshelf.objects.get(name=name, user=self.user)
        except Bookshelf.DoesNotExist:
            return name
        print(name)
        raise forms.ValidationError('Shelf %s already exists'%name)

    def save(self, commit=True):
        # user = super(RegistrationForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.email = self.cleaned_data['email']

        if commit:
            shelf = Bookshelf.objects.create(
            name = self.cleaned_data['name'],
            user = self.user

        )



class RegistrationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150,required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, help_text='First Name',required=True)
    last_name = forms.CharField(max_length=100, help_text='Last Name',required=True)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput,required=True)

    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',



        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exists")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Email already exists")

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            print("yo")
            raise forms.ValidationError("password and confirm password does not match")


    def save(self, commit=True):
        # user = super(RegistrationForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.email = self.cleaned_data['email']

        if commit:
            user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']

        )

        return user


class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
