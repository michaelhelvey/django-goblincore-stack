from bs4 import BeautifulSoup
from bs4.element import Tag
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    def getBySelectorOrFail(self, response, selector) -> Tag:
        element = self.getBySelector(response, selector)
        self.assertIsNotNone(element)
        self.assertIsInstance(element, Tag)

        return element

    def getBySelector(self, response, selector) -> Tag:
        soup = self.getSoup(response)
        element = soup.select_one(selector)
        return element

    def getSoup(self, response):
        return BeautifulSoup(response.content, "html.parser")

    def assertLinkGoesToTitle(self, response, selector, title):
        link = self.getBySelectorOrFail(response, selector)
        response = self.client.get(link["href"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.getSoup(response).title.text.strip(), title)

    def assertLinkGoesToUrl(self, response, selector, url):
        link = self.getBySelectorOrFail(response, selector)
        response = self.client.get(link["href"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, url)

    def assertSelectorDoesNotExist(self, response, selector):
        element = self.getBySelector(response, selector)
        self.assertIsNone(element)
