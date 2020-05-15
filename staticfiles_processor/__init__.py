default_app_config = 'staticfiles_processor.apps.StaticfilesProcessorApp'


class StaticfileProcessor(object):
    def check_match(self, path, match):
        raise NotImplementedError()

    def process(self, destination, origin):
        raise NotImplementedError()
