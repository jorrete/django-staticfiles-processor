from django.contrib.staticfiles.finders import AppDirectoriesFinder, FileSystemFinder
from django.core.files.storage import FileSystemStorage

from .settings import STATICFILES_BUILD
from .process import process_path
from .utils import empty_dir


staticfiles_processor_storage = FileSystemStorage(location=STATICFILES_BUILD)
empty_dir(staticfiles_processor_storage.base_location)


class ProcessedFinderMixin(object):
    def find(self, path, all=False):
        matches = super().find(path, all)
        if not matches or not len(matches):
            return matches
        matches = [process_path(path, match) for match in ([matches] if type(matches) != list else matches)]
        return matches if all else matches[0]

    def list(self, ignore_patterns):
        for item in super().list(ignore_patterns):
            path, storage = item
            match = storage.path(path)
            result_path = process_path(path, match)
            yield path, staticfiles_processor_storage if result_path != match else storage


class ProcessedFileSystemFinder(ProcessedFinderMixin, FileSystemFinder):
    pass


class ProcessedAppDirectoriesFinder(ProcessedFinderMixin, AppDirectoriesFinder):
    pass
