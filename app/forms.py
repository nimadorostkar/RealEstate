from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Contact
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from . import models


#------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['phone','additional_information','user_photo', 'user_type']


#------------------------------------------------------------------------------
class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']






#------------------------------------------------------------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'phone', 'body')





# End
