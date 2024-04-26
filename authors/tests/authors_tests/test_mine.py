from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

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

class BecomingIndependentTest(TestCase):
    
    def test_user_form_raises_error_if_same_username(self):
        create_test_user(username="sameuser")
        with self.assertRaises(IntegrityError):
            create_test_user(username="sameuser")

    def test_user_form_saves_users_correctly(self):
        create_test_user()
        create_test_user()
        self.assertEqual(len(User.objects.all()),2)