from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attr} {attr_new_val}".strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, "placeholder", placeholder_val)

def strong_password(password):
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")
    if not regex.match(password):
        raise ValidationError((
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters."
        ),
            code="invalid"
        )

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"].widget.attrs["placeholder"] = "Your username"
        add_placeholder(self.fields["username"],"Your username...")
        add_placeholder(self.fields["email"],"Your existing e-mail...")
        add_placeholder(self.fields["last_name"],"All that comes after the first name kkk")
        add_attr(self.fields["username"],"css", "a-css-class")

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Make sure you won't forget it..."
            }
        ),
        error_messages={
            "required":"Password must not be empty."
        },
        validators=[
            strong_password,
        ],
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder":"Repeat the same password."
        }),
        label="Password confirmation",
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        # exclude = ["first_name"]
        labels = {
            "username":"Username",
            "first_name":"First name",
            "last_name":"Last name",
            "email":"E-mail",
            "password":"Password",
        }
        help_texts = {
            "email":"The e-mail must be valid."
        }
        error_messages = {
            "username":{
                "required":"This field must not be empty.",
            }
        }
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder":"Your first name...",
                "class": "",
            }),
            "password": forms.PasswordInput(attrs={
                "placeholder":"Make sure you won't forget it..."
            })
        }
    
    # VALIDAÇÃO DE CAMPO
    def clean_password(self):
        data = self.cleaned_data.get("password")

        if "atenção" in data:
            raise ValidationError(
                "Não digite a palavra '%(value)s'",
                code="invalid",
                params={"value":"atenção"}
            )

        return data
    
    # VALIDAÇÃO DO FORM COMO UM TODO
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            # ESTE CÓDIGO FUNCIONA, VOU ESCREVER OUTRO PRA REGISTRAR O QUE O PROFESSOR PASSOU
            # raise ValidationError({
            #     "password":"Password and Password2 must be equal",
            #     "password2":"Password and Password2 must be equal",
            # })
            password_confirmation_error = ValidationError(
                    "Password and Password2 must be equal",
                    code="invalid"
                )
            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [
                    password_confirmation_error,
                    # "another error"
                ]
            })