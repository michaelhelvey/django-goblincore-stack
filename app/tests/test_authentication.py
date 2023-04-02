from app.factories import UserFactory
from app.utils.test import TestCase


class UserHomePageTest(TestCase):
    def test_home_page_shows_login_link_to_logged_out_user(self):
        response = self.client.get("/")
        login_link = self.getBySelectorOrFail(response, "a#login-link")
        self.assertEqual(
            login_link.text,
            "Log In",
            "expected the home page to show a log in link to a logged out user",
        )

        self.assertSelectorDoesNotExist(response, "a#logout-link")

        self.assertLinkGoesToTitle(response, "a#login-link", "Log In")

    def test_home_page_shows_log_out_link_to_signed_in_user(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/")
        self.assertSelectorDoesNotExist(response, "a#login-link")

        self.assertLinkGoesToTitle(response, "a#logout-link", "Log Out")


class LoginTestCase(TestCase):
    def test_user_can_log_in(self):
        passwd = "1234'"
        user = UserFactory(password=passwd)

        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.getSoup(response).title.text.strip(), "Log In")

        response = self.client.post(
            "/accounts/login/", {"login": user.email, "password": passwd}
        )

        # On successful login, the user should be redirected to the profile page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/")

    def test_user_login_page(self):
        response = self.client.get("/accounts/login/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.getSoup(response).title.text.strip(), "Log In")

        # assert that we have a valid link to the sign up page
        self.assertLinkGoesToTitle(
            response, "a#create-account-link", "Create Account"
        )
