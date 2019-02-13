import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()

setup(
    name='django-locking',
    version='2.3.1',
    description=("Prevents users from doing concurrent editing in Django. Works out of the box in the admin interface, or you can integrate it with your own apps using a public API."),
    long_description=long_description,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities'],
    keywords='locking mutex',
    author='Richard Cooke et al',
    author_email='rcooke@tnky.ca',
    url='http://www.github.com/rcooke/django-locking/',
    download_url='http://www.github.com/rcooke/django-locking/tarball/master',
    license='BSD',
    packages=find_packages(),
    package_data={
        'locking': [
            'static/locking/js/*',
            'static/locking/img/*',
            'static/locking/css/*',
        ]
    },
    install_requires=['django-staticfiles','simplejson'],
)

