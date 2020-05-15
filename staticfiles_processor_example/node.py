from os.path import dirname

from django.conf import settings

from staticfiles_processor.utils import run, get_modules_paths
from staticfiles_processor import StaticfileProcessor


def node_processor(node_bin, node_script, src, dest, node_modules_path=None, paths=[]):
    command = [
        node_bin,
        node_script,
        '--src', src,
        '--dest', dest,
        '--paths', ','.join(paths),
    ]

    if settings.DEBUG:
        command.append('--debug')

    return run(command, env={
        'NODE_PATH': node_modules_path,
    })


class RollupProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return path.endswith('.rollup.js')

    def process(self, destination, origin):
        node_processor(
            settings.NODE_BIN_PATH,
            settings.ROLLUP_PROCESSOR_PATH,
            destination,
            destination,
            node_modules_path=settings.NODE_MODULES_PATH,
            paths=[dirname(origin), ] + get_modules_paths() + [settings.NODE_MODULES_PATH, ])


class PostcssProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return path.endswith('.postcss.css')

    def process(self, destination, origin):
        node_processor(
            settings.NODE_BIN_PATH,
            settings.POSTCSS_PROCESSOR_PATH,
            destination,
            destination,
            node_modules_path=settings.NODE_MODULES_PATH,
            paths=[dirname(origin), ] + get_modules_paths() + [settings.NODE_MODULES_PATH, ])
