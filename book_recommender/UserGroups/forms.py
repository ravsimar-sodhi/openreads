<<<<<<< HEAD
from django import forms
# from Users.models import User
from UserGroups.models import *
from Users.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class GroupCreationForm(forms.ModelForm):
    # group_name = forms.CharField(label='Group Name')
    # group_description = forms.TextField(required=False, label='Group Description')
    # group_pic = forms.ImageField()
    
    class Meta:
        model = UserGroup

        fields = (
            'group_name',
            'group_description',
            'group_pic'



        )


    def save(self,request, commit=True):

        if commit:
            userGroup = UserGroup.objects.create(
            group_name = self.cleaned_data['group_name'],
            group_description = self.cleaned_data['group_description'],
            group_pic = self.cleaned_data['group_pic'],
            group_creator = request.user
        )
            groupMember = GroupMember.objects.create(
                user = request.user,
                group = userGroup
            )

        return userGroup


# class EditProfileForm(UserChangeForm):
#     template_name='/something/else'

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'first_name',
#             'last_name',
#             'password'
#         )
=======
from django import forms
# from Users.models import User
from UserGroups.models import *
from Users.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class GroupCreationForm(forms.ModelForm):
    # group_name = forms.CharField(label='Group Name')
    # group_description = forms.TextField(required=False, label='Group Description')
    # group_pic = forms.ImageField()
    
    class Meta:
        model = UserGroup

        fields = (
            'group_name',
            'group_description',
            'group_pic'



        )


    def save(self,request, commit=True):

        if commit:
            userGroup = UserGroup.objects.create(
            group_name = self.cleaned_data['group_name'],
            group_description = self.cleaned_data['group_description'],
            group_pic = self.cleaned_data['group_pic'],
            group_creator = request.user
        )
            groupMember = GroupMember.objects.create(
                user = request.user,
                group = userGroup
            )

        return userGroup


# class EditProfileForm(UserChangeForm):
#     template_name='/something/else'

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'first_name',
#             'last_name',
#             'password'
#         )
>>>>>>> 7003b5a659b47ff10a98f9fa5808c8f11b231424
