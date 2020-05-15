import json

from django.test import TestCase
from django.contrib.staticfiles import finders
from staticfiles_processor.utils import read_file


class FindTest(TestCase):
    def test_file_not_matching(self):
        """Check if can find a file not to be processed"""
        self.assertIsNotNone(finders.find('myapp/js/index.js'))

    def test_file_matching(self):
        """Check if can find a file to be processed"""
        path = finders.find('myapp/css/index.postcss.css')
        self.assertIsNotNone(path)
        self.assertRegex(read_file(path), 'blue')


class MultipleMatchTest(TestCase):
    def test_file_matching(self):
        """Check if file is being processed by two processors"""
        path = finders.find('mydata.json')
        self.assertIsNotNone(path)
        content = json.loads(read_file(path))
        self.assertEqual(content['name'], 'staticfiles_processor')
        self.assertEqual(content['description'], 'Cool Django app.')
