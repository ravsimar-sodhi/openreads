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

class AddGroupShelfForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
         if len(args)>1:
            self.group = int(args[1])
         kwargs.pop('group',None)
         super(AddGroupShelfForm, self).__init__(*args, **kwargs)
    name = forms.CharField(label="Shelf Name",min_length=4, max_length=256)
    class Meta:
        model = Groupshelf
        
        fields = (
            'name'
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            shelf = Groupshelf.objects.get(name=name, group=UserGroup.objects.filter(id=self.group)[0])
        except Groupshelf.DoesNotExist:
            return name
        print(name)
        raise forms.ValidationError('Shelf %s already exists'%name)
    
    def save(self, commit=True):
        # user = super(RegistrationForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.email = self.cleaned_data['email']

        if commit:
            shelf = Groupshelf.objects.create(
            name = self.cleaned_data['name'],
            group = UserGroup.objects.filter(id=self.group)[0]
            
        )
