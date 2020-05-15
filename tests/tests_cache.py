import time

from django.test import TestCase
from django.contrib.staticfiles import finders


class CacheTest(TestCase):
    def test_file_cache(self):
        """Check if can find a file to be processed"""
        start = time.time()
        path = finders.find('dumb.file')
        end = time.time()
        self.assertIsNotNone(path)
        self.assertGreater(end - start, 1)

        start = time.time()
        path = finders.find('dumb.file')
        end = time.time()
        self.assertIsNotNone(path)
        self.assertLess(end - start, 0.1)
