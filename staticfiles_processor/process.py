from os.path import exists, dirname, join
from os import utime

from django.utils.module_loading import import_string

from .utils import copy_file, mkdir, get_stat
from .settings import STATICFILES_BUILD, STATICFILES_PROCESSORS, STATICFILES_PROCESSORS_CACHE, logger


processors = [(import_string(p) if type(p) == str else p)() for p in STATICFILES_PROCESSORS]


def match_has_changed(path, match):
    match_stat = get_stat(match)
    processed_stat = get_stat(path)

    if processed_stat is None:
        return True

    return match_stat.st_mtime != processed_stat.st_mtime


def process_path(path, match):
    matched_processors = [
            p for p in processors
            if p.check_match(path, match)]

    logger.info('[staticfiles_processor] {}'.format(path))

    if not len(matched_processors):
        return match

    processed_path = join(STATICFILES_BUILD, path)

    if not exists(processed_path):
        mkdir(dirname(processed_path))
        copy_file(match, processed_path)

    if not STATICFILES_PROCESSORS_CACHE or match_has_changed(match, processed_path):
        copy_file(match, processed_path)
        for p in matched_processors:
            p.process(processed_path, match)

        match_stat = get_stat(match)
        utime(processed_path, (match_stat.st_atime, match_stat.st_mtime))

    return processed_path
