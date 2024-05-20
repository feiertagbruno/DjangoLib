from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password, add_attr

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"].widget.attrs["placeholder"] = "Your username"
        add_placeholder(self.fields["username"],"Your username...")
        add_placeholder(self.fields["email"],"Your existing e-mail...")
        add_placeholder(self.fields["last_name"],"All that comes after the first name kkk")
        add_placeholder(self.fields["first_name"],"Your first name...")
        add_attr(self.fields["username"],"css", "a-css-class")

    first_name = forms.CharField(
        error_messages={"required":"Write your first name"},
        required=True,
        label="First name",
    )

    last_name = forms.CharField(
        error_messages={"required":"Write your last name"},
        required=True,
        label="Last name",
    )

    username = forms.CharField(
        label="Username",
        required=True,
        error_messages={
            "required":"This field must not be empty",
            "min_length":"Username must have at least 4 characters",
            "max_length":"Username must not have more than 150 characters",
            },
        help_text=(
            "Username may have letters, numbers or one of those chars @.*-_ ."
            "The length should be between 4 and 150 characters."
        ),
        min_length=4, max_length=150,
    )

    email = forms.CharField(
        error_messages={"required":"Your e-mail is needed"},
        required=True,
        label="E-mail",
        help_text="The e-mail must be valid.",
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Make sure you won't forget it..."
            }
        ),
        error_messages={
            "required":"Password must not be empty"
        },
        validators=[
            strong_password,
        ],
        help_text=(
            "Needed at least: 1 uppercase, 1 lowercase and 1 number"
        ),
        label="Password"
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder":"Repeat the same password."
        }),
        label="Password confirmation",
        error_messages={"required":"This field must not be empty"}
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
    #     # exclude = ["first_name"]
    #     labels = {
    #         "username":"Username",
    #     }
    #     error_messages = {
    #         "username":{
    #             "required":"This field must not be empty",
    #         }
    #     }
        # widgets = {
        #     "first_name": forms.TextInput(attrs={
        #         "placeholder":"Your first name...",
        #     }),
        # }
    
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
    
    def clean_email(self):
        email = self.cleaned_data.get("email","")
        exists = User.objects.filter(email = email).exists()

        if exists:
            raise ValidationError(
                "User e-mail is already in use", code="invalid",
            )
        return email
    
    # VALIDAÇÃO DO FORM COMO UM TODO
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2 and password != None and password2 != None:
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
