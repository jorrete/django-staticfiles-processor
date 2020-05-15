# django-staticfiles-processor (alpha)

## Install

```bash
pip install django-staticfiles-processor
```

## Description

Inspired in the old [django-staticfilesplus](https://github.com/evansd/django-staticfilesplus) package.

Allows you to configure a series of **processors** that allow you to transform the static files before are served or collected. Each file will cascade through the processors and processed only when the path matches.

## settings
```python
STATICFILES_PROCESSORS = [
    # your processors
]

STATICFILES_FINDERS = [
    'staticfiles_processor.finders.ProcessedAppDirectoriesFinder',
    'staticfiles_processor.finders.ProcessedFileSystemFinder',
]

TMP_DIR = '/tmp' # default: /tmp

STATICFILES_BUILD = 'staticfiles_build' # default: staticfiles_build

STATICFILES_PROCESSORS_CACHE = True # default: False
```

## processor

``` python
import time

from staticfiles_processor import StaticfileProcessor


class WaitProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return path == 'dumb.file'

    def process(self, destination, origin):
        time.sleep(1)
```

The processor class must have two methods:

### check_match

- path: static path, e.g. 'myapp/js/myfile.js'
- match: file path, e.g. '/my/static/root/myapp/js/myfile.js'

### process

- destination: file path, e.g.'/my/tmp/dir/staticfiles_build/myapp/js/myfile.js'
- origin: file path, e.g. '/my/static/root/myapp/js/myfile.js'

The processors should overwrite destination, you read **destination** do you stuff and write to **destination**.

If you don't want to read the whole file to memory and write it at once you should manage your temporary file in other place.

Processor are dumb and expect you to manage everything. It doesn't handle exceptions so if it fails it will halt execution.

## cache
Caching works by checking changes in the modification date of the origin file and it's cleared each restart.

If you are using, let's say, rollup to bundle you javascript, it will not be aware of changes of you imports so as long of the static files remain unchanged it will keep returning the cached file.

## Development

### Install

```bash
git clone https://github.com/jorrete/django-staticfiles-processor
./create_venv
. venv/bin/activate
cd django-staticfiles-processor/myexample
./manage.py migrate
./manage.py runserver
```

### Test

```bash
cd django-cache-helpers
tox
```

### Examples
Check the examples modules to see possibilities.

```python
STATICFILES_PROCESSORS = [
    'staticfiles_processor_example.node.RollupProcessor',
    'staticfiles_processor_example.node.PostcssProcessor',
    'staticfiles_processor_example.image.ImageProcessor',
    'staticfiles_processor_example.text.NameProcessor',
]
```

#### staticfiles_processor_example.node.RollupProcessor

Bundle javascript and import from django static folders and from node_modules folder.

#### staticfiles_processor_example.node.PostcssProcessor

Bundle css and import from django static folders and from node_modules folder.

#### staticfiles_processor_example.image.ImageProcessor

Resize and add background to png images using arguments embedded in the filename.

#### staticfiles_processor_example.image.NameProcessor

Replace text of the file.
