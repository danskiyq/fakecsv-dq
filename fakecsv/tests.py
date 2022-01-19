from django.test import TestCase, Client
from django.urls import reverse


class SchemaTest(TestCase):
    """Just a few simple tests to prevent reloading pages each change I do"""

    def test_page_loads(self):
        client = Client()
        self.assertEqual(client.get(reverse('fakecsv:create')).status_code, 302, "fakecsv:create doesn't loads")
        self.assertEqual(client.get(reverse('fakecsv:main')).status_code, 200, "fakecsv:create doesn't loads")
