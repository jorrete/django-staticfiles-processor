from staticfiles_processor import StaticfileProcessor
from staticfiles_processor.utils import read_file, write_file


class ReplaceProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return path == 'mydata.json'

    def process(self, destination, origin):
        content = read_file(destination)
        write_file(destination, content.replace(self.from_text, self.to_text))


class NameProcessor(ReplaceProcessor):
    from_text = 'staticfiles'
    to_text = 'staticfiles_processor'


class DescriptionProcessor(ReplaceProcessor):
    from_text = 'Django app.'
    to_text = 'Cool Django app.'
