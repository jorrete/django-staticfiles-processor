from setuptools import setup


setup(name='django-processed-staticfiles',
      version='0.1.0',
      description='',
      url='https://github.com/jorrete/django-processed-staticfiles/',
      author='Jorge Rodríguez-Flores Esparza',
      author_email='jorrete@gmail.com',
      license='MIT',
      packages=['staticfiles_processor', ],
      include_package_data=True,
      install_requires=[
          'django',
          'pillow',
      ],
      dependency_links=[],
      zip_safe=False)
