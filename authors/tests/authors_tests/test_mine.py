from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.urls import reverse
from authors.forms import RegisterForm
from django.core.exceptions import ValidationError

def create_test_user(
    first_name = "Resu",
    last_name = "Tset",
    username = "resutset",
    email = "email@email.com",
    password = "Abc12345678"
):
    i = 1
    if username != "sameuser":
        while len(User.objects.filter(username=username)) != 0:
            username = f"{username}{i}"
            i += 1
    user = User.objects.create(
        first_name = first_name,
        last_name = last_name,
        username = username,
        email = email,
        password = password
    )
    return user

def make_dict_user(
    first_name = "test",
    last_name = "user",
    username = "testuser",
    email = "email@email.com",
    password = "Abc123456",
    password2 = "Abc123456"
):
    return {
    "first_name": first_name,
    "last_name": last_name,
    "username": username,
    "email": email,
    "password": password,
    "password2": password2
    }

class BecomingIndependentTest(TestCase):
    
    def test_user_form_raises_error_if_same_username(self):
        create_test_user(username="sameuser")
        with self.assertRaises(IntegrityError):
            create_test_user(username="sameuser")

    def test_user_form_saves_users_correctly(self):
        create_test_user()
        create_test_user()
        self.assertEqual(len(User.objects.all()),2)
    
    def test_user_form_if_form_returns_error_messages_correctly(self):
        data_form = {
            "first_name":"Brono",
            "last_name":"Martono",
            "username":"bronomartono",
            "email":"email@email.com",
            "password":"Abc123456",
            "password2":"Abc123456",
        }
        form = RegisterForm(data_form)
        self.assertTrue(form.is_valid())
    
    def test_user_form_password_validation_strong_password(self):
        dict_user = make_dict_user(password="123",password2="123")
        form = RegisterForm(dict_user)
        self.assertIn(
            "Password must have at least one uppercase letter", 
            form.errors["password"][0]
        )
    
    def test_user_form_password_validation_same_password(self):
        dict_user = make_dict_user(password="Abc123456",password2="Abc123455")
        form = RegisterForm(dict_user)
        self.assertIn(
            "Password and Password2 must be equal", 
            form.errors["password"][0]
        )
