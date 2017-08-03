from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='retort',
    version='0.1',
    description="A lightweight web framework for AWS API Gateway + Lambda.",
    long_description=long_description,
    url='https://github.com/timsavage/retort',
    author='Tim Savage',
    author_email='tim@savage.company',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: BSD License',

        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='python web framework lambda aws api-gateway',

    packages=find_packages(include=('retort',)),

    install_requires=['boto3', 'markupsafe'],
    extras_require={
        'development': ['werkzeug']
    },
)
