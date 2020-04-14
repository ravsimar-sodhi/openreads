from django import forms
# from Users.models import User
from UserGroups.models import *
from Users.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError



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

    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        try:
            group = UserGroup.objects.get(group_name=group_name)
        except UserGroup.DoesNotExist:
            return group_name
        raise forms.ValidationError("Group Already Exists!")


    def save(self,request, commit=True):

        if commit:
            userGroup = UserGroup.objects.create(
                group_name = self.cleaned_data['group_name'],
                group_description = self.cleaned_data['group_description'],
                group_pic = self.cleaned_data['group_pic'],
                group_creator = request.user
            )

            userGroup.group_members.add(request.user)
            # print("group created successfully")
            # for member in userGroup.group_members.all():
                # print(member.username)
            # groupMember = GroupMember.objects.create(
            #     user = request.user,
            #     group = userGroup
            # )

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
