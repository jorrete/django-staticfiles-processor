import errno
import os
import subprocess
from shutil import copyfile, rmtree

from django.conf import settings
from django.apps import apps


def get_stat(path):
    try:
        return os.stat(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def delete_dir(path):
    try:
        rmtree(path)
    except OSError as e:
        if e.errno not in [errno.EEXIST, errno.ENOENT]:
            raise


def empty_dir(path):
    delete_dir(path)
    mkdir(path)


def read_file(path, mode='r'):
    with open(path, mode) as f:
        return f.read()


def write_file(path, content='', mode='w'):
    with open(path, mode) as f:
        f.write(content)


def copy_file(origin, destination):
    copyfile(origin, destination)


def run(command, env={}):
    custom_env = os.environ.copy()
    custom_env.update(env)
    p = subprocess.Popen(command, env=custom_env, stdout=subprocess.PIPE)
    out, err = p.communicate()

    if settings.DEBUG and len(out):
        print(out)

    if err or p.returncode != 0:
        em = 'return code: {0}, error: {1}'.format(
                p.returncode,
                err,
        )
        raise Exception(em)


def get_modules_paths():
    paths = []
    app_configs = apps.get_app_configs()

    for finder in settings.STATICFILES_FINDERS:
        if 'ProcessedFileSystemFinder' in finder:
            for app_config in app_configs:
                path = os.path.join(app_config.path, 'static')
                if os.path.exists(path):
                    paths.append(path)

        if 'ProcessedAppDirectoriesFinder' in finder:
            paths.extend(settings.STATICFILES_DIRS)

    return paths
