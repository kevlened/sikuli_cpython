from setuptools import setup, find_packages
import sys

# Temporarily download dependencies from my own host
github = "https://github.com/kevlened/pyjnius/releases/download"

if sys.platform == 'win32':
    dependency_links = [
        github + "/v1.1/jnius-1.1-dev.win32-py2.7.exe"
    ]
else:
    dependency_links = [
        github + "/v1.1/jnius-1.1-dev.tar.gz"
    ]

setup(
    name='sikuli',
    version='0.1',
    description='A CPython wrapper around the sikuli standalone jar',
    author='Len Boyette',
    author_email='boyettel+sikuli@gmail.com',
    url='https://github.com/kevlened/sikuli_cpython',
    packages=['sikuli'],
    keywords=['testing'],
    requires=['jnius'],
    package_data={'': ['sikuli-api-1.0.2-standalone.jar']},
    include_package_data=True,
    setup_requires=['jnius >= 1.1-dev'],
    install_requires=['jnius >= 1.1-dev'],
    dependency_links = dependency_links,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta'
    ]
     )

# To update pypi: 'python setup.py register sdist bdist_wininst upload'