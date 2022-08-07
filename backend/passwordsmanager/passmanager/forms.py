from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput

from .models import *
from .validators import (
    has_lower_case,
    has_number,
    has_symbol,
    has_upper_case,
    similariy_validator,
    validate_minimum_length,
    validate_not_common_password,
    validate_not_numeric,
)


class EntryForm(forms.Form):
    entrysite = forms.CharField(max_length=70)
    entryemail = forms.CharField(max_length=70)
    entrypassword = forms.CharField(max_length=70)
    masterpassword = forms.CharField(max_length=70)


class MasterPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MasterPasswordForm, self).__init__(*args, **kwargs)

    last_master = forms.CharField(
        max_length=70,
        label='Your master password',
        widget=TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Your master password',
                'autofocus': True,
            }
        ),
    )

    master = forms.CharField(
        max_length=70,
        label='Your new master password',
        validators=[
            validate_minimum_length,
            validate_not_numeric,
            validate_not_common_password,
            has_lower_case,
            has_upper_case,
            has_number,
            has_symbol,
        ],
        widget=TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Your new master password',
            }
        ),
    )

    master_confirm = forms.CharField(
        max_length=70,
        label='Confirm your new master password',
        widget=TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Confirm your new master password',
            }
        ),
    )

    def clean_master(self):
        password = self.cleaned_data.get('master')
        similariy_validator(password, self.user)
        return password


class MasterCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MasterCreateForm, self).__init__(*args, **kwargs)

    master = forms.CharField(
        max_length=70,
        label='Define a new master password',
        validators=[
            validate_minimum_length,
            validate_not_numeric,
            validate_not_common_password,
            has_lower_case,
            has_upper_case,
            has_number,
            has_symbol,
        ],
        widget=TextInput(
            attrs={
                'autocomplete': 'off',
                'autofocus': True,
                'placeholder': 'Define a new master password',
            }
        ),
    )
    master_confirm = forms.CharField(
        max_length=70,
        label='Confirm your new master password',
        widget=TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Confirm your new master password',
            }
        ),
    )

    def clean_master(self):
        password = self.cleaned_data.get('master')
        similariy_validator(password, self.user)
        return password
