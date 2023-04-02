from django.shortcuts import reverse

from app.factories import UserFactory
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
