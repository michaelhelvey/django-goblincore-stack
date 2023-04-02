import re

from allauth.account.models import EmailAddress
from django.shortcuts import reverse

from app.factories import UserFactory
from app.models import User
from app.utils.test import TestCase


class UserHomePageTest(TestCase):
    def test_home_page_shows_login_link_to_logged_out_user(self):
        response = self.client.get(reverse("home"))
        login_link = self.getBySelectorOrFail(response, "a#login-link")
        self.assertEqual(login_link.text, "Log In")

        self.assertSelectorDoesNotExist(response, "a#logout-link")
        self.assertLinkGoesToUrl(
            response, "a#login-link", reverse("account_login")
        )

    def test_home_page_shows_log_out_link_to_logged_in_user(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(reverse("home"))
        self.assertSelectorDoesNotExist(response, "a#login-link")
        self.assertLinkGoesToUrl(
            response, "a#logout-link", reverse("account_logout")
        )


class LoginTest(TestCase):
    def test_user_can_log_in(self):
        passwd = "1234"
        user = UserFactory(password=passwd)

        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.getSoup(response).title.text.strip(), "Log In")

        response = self.client.post(
            "/accounts/login/", {"login": user.email, "password": passwd}
        )

        # On successful login, the user should be redirected to the profile page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("profile"))

    def test_user_login_page_links(self):
        response = self.client.get(reverse("account_login"))

        self.assertEqual(response.status_code, 200)
        self.assertPageHasTitle(response, "Log In")

        # assert that we have a valid link to the sign up page
        self.assertLinkGoesToUrl(
            response, "a#create-account-link", reverse("account_signup")
        )


class CreateAccountTest(TestCase):
    def test_user_can_create_account_and_verify_email(self):
        url = reverse("account_signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertPageHasTitle(response, "Create Account")

        passwd = "asdf1234*"
        user_form = UserFactory.build(password=passwd)

        response = self.client.post(
            url,
            {
                "email": user_form.email,
                "first_name": user_form.first_name,
                "last_name": user_form.last_name,
                "password1": passwd,
                "password2": passwd,
            },
        )

        user = User.objects.get(email=user_form.email)
        email_addr = EmailAddress.objects.get(email=user_form.email)

        self.assertEqual(email_addr.verified, False)

        self.assertEqual(user.email, user_form.email)
        self.assertEqual(user.first_name, user_form.first_name)
        self.assertEqual(user.last_name, user_form.last_name)
        self.assertEqual(user.is_active, True)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse("account_email_verification_sent")
        )

        response = self.client.get(response.url)
        self.assertPageHasTitle(response, "Verify Your Email Address")

        email = self.getLastEmail()
        license_link_regex = r"go to (http:.*/accounts/confirm-email/.*)\n"
        license_link = re.search(license_link_regex, email.body).group(1)

        response = self.client.get(license_link)
        self.assertEqual(response.status_code, 200)

        self.assertPageHasTitle(response, "Confirm Email Address")
        self.assertEqual(
            self.getBySelectorOrFail(
                response, "button#confirm-address-button"
            ).text,
            "Confirm",
        )

        # We expect the user to be logged in when the confirm their email:
        self.client.force_login(user)

        response = self.client.post(license_link)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("profile"))

        email_addr.refresh_from_db()
        self.assertEqual(email_addr.verified, True)
