from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.forms import fields, widgets
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from . models import Address
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password(Again)')
    # first_name = models.CharField(_('first name'), max_length=150, blank=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name']
        widgets = {'username':forms.EmailInput(attrs={'class':'form-control','readonly':True}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        }

        error_messages = {
            'first_name':{'required':'This field is required.'},
            'last_name':{'required':'This field is required.'}
        }
        labels = {'username':'Email'}

class MyLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}),label="Email")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'class':'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'})
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street','village','district','state','pin_code','mobile']
        widgets = {'street':forms.TextInput(attrs={'class':'form-control'}),
        'street':forms.TextInput(attrs={'class':'form-control'}),
        'village':forms.TextInput(attrs={'class':'form-control'}),
        'district':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-select'}),
        'pin_code':forms.NumberInput(attrs={'class':'form-control'}),
        'mobile':forms.NumberInput(attrs={'class':'form-control'})
        }

        labels = {'district':'distic','mobile':'Mobile Number'}