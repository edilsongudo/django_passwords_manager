from django import forms
from django.forms.widgets import TextInput, PasswordInput
from django.core.exceptions import ValidationError
from .models import *
from .validators import (
    validate_minimum_length,
    validate_not_numeric,
    validate_not_common_password,
    similariy_validator,
    has_lower_case,
    has_upper_case,
    has_number,
    has_symbol
)


class MasterPasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MasterPasswordForm, self).__init__(*args, **kwargs)

    last_master = forms.CharField(
        max_length=70,
        label='Your master password',
        widget=TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Your master password',
            'autofocus': True
        }
        )
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
            has_symbol
        ],
        widget=TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Your new master password'
        }
        )
    )

    master_confirm = forms.CharField(
        max_length=70,
        label='Confirm your new master password',
        widget=TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Confirm your new master password'
        }
        )
    )

    def clean(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('master')
        password_confirm = self.cleaned_data.get('master_confirm')

        if password != password_confirm:
            raise ValidationError(
                'Fields Master Password and master password confirm do not match')

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
            has_symbol
        ],
        widget=TextInput(attrs={
            'autocomplete': 'off',
            'autofocus': True,
            'placeholder': 'Define a new master password'
        }
        )
    )
    master_confirm = forms.CharField(
        max_length=70,
        label='Confirm your new master password',
        widget=TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Confirm your new master password'
        }
        )
    )

    def clean(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('master')
        password_confirm = self.cleaned_data.get('master_confirm')

        if password != password_confirm:
            raise ValidationError(
                'Fields Master Password and master password confirm do not match')

    def clean_master(self):
        password = self.cleaned_data.get('master')
        similariy_validator(password, self.user)
        return password
