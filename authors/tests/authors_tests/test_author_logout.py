from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username="myuser", password="mypass")
        
        self.client.login(username="myuser", password="mypass")

        response = self.client.get(reverse("authors:logout"),follow=True)
        print(response.content.decode("utf-8"))

        self.assertIn("You are logged in with ", response.content.decode("utf-8"))
    
    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username="myuser", password="mypass")
        
        self.client.login(username="myuser", password="mypass")

        response = self.client.post(
            reverse("authors:logout"),
            data={
                "username":"another_user"
            },
            follow=True
        )

        self.assertIn("You are logged in with ", response.content.decode("utf-8"))

    def test_user_logout_successfully(self):
        User.objects.create_user(username="myuser", password="mypass")
        
        self.client.login(username="myuser", password="mypass")

        response = self.client.post(
            reverse("authors:logout"),
            data={
                "username":"myuser"
            },
            follow=True
        )

        self.assertIn("Logged out successfully", response.content.decode("utf-8"))
