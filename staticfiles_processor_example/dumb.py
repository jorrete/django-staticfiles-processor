import time

from staticfiles_processor import StaticfileProcessor


class WaitProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return path == 'dumb.file'

    def process(self, destination, origin):
        time.sleep(1)
