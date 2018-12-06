import os
from distutils.core import setup
from subprocess import check_call

from setuptools.command.develop import develop


class CloneGitSubmodules(develop):
    def run(self):
        if os.path.exists('.git'):
            check_call(['git', 'submodule', 'update', '--init'])
        super(CloneGitSubmodules, self).__init__()


setup(
    name='django-dajaxice-py3dj2',
    version='0.8.2',
    author='Antonio Tomasic',
    author_email='atomasic@gmail.com',
    description='Agnostic and easy to use ajax library for django',
    url='https://github.com/atomasic/django-dajaxice',
    license='BSD',
    packages=['dajaxice',
              'dajaxice.templatetags',
              'dajaxice.core'],
    package_data={'dajaxice': ['templates/dajaxice/*']},
    long_description=("Easy to use AJAX library for django, all the "
                      "presentation logic resides outside the views and "
                      "doesn't require any JS Framework. Dajaxice uses the "
                      "unobtrusive standard-compliant (W3C) XMLHttpRequest "
                      "1.0 object."),
    install_requires=[
        'Django>=2.1.3'
    ],
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities'],
    python_requires='>=3.6.7',
    cmd_class={"develop": CloneGitSubmodules}
)
