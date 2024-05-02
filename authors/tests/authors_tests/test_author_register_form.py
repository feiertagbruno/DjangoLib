from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ("username","Your username..."),
        ("email","Your existing e-mail..."),
        ("last_name","All that comes after the first name kkk"),
        ("password","Make sure you won't forget it..."),
        ("password2","Repeat the same password."),
        ("first_name","Your first name..."),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        placeholder_field = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, placeholder_field)

    @parameterized.expand([
        ("email","The e-mail must be valid."),
        ("password","Needed at least: 1 uppercase, 1 lowercase and 1 number"),
        ("username",(
            "Username may have letters, numbers or one of those chars @.*-_ ."
            "The length should be between 4 and 150 characters."
            )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ("username","Username"),
        ("email","E-mail"),
        ("first_name","First name"),
        ("last_name","Last name"),
        ("password","Password"),
        ("password2","Password confirmation"),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password":"Str0ngP@assword1",
            "password2":"Str0ngP@assword1",
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ("username","This field must not be empty"),
        ("first_name","Write your first name"),
        ("last_name","Write your last name"),
        ("email","Your e-mail is needed"),
        ("password","Password must not be empty"),
        ("password2","This field must not be empty"),
    ])
    def test_fields_cannot_be_empty(self,field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data = self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_username_field_min_length_should_be_4(self):
        self.form_data["username"] = "joa"
        url = reverse("authors:create")
        response = self.client.post(url, data = self.form_data, follow=True)
        msg = "Username must have at least 4 characters"
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_username_field_max_length_should_be_150(self):
        self.form_data["username"] = "a" * 150
        url = reverse("authors:create")
        response = self.client.post(url, data = self.form_data, follow=True)
        msg = "Username must not have more than 150 characters"
        self.assertNotIn(msg, response.content.decode("utf-8"))

        self.form_data["username"] = "a" * 151
        response = self.client.post(url, data = self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse("authors:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_email_field_must_be_unique(self):
        url = reverse("authors:create")
        self.client.post(url,data=self.form_data,follow=True)
        response = self.client.post(url,data=self.form_data,follow=True)
        msg = "User e-mail is already in use"
        self.assertIn(msg, response.context["form"].errors.get("email"))
        self.assertIn(msg, response.content.decode("utf-8"))