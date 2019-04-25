from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='twtrgrep',
    version='1.0',
    description='A grep-like tool for searching tweets.',
    long_description=long_description,
    url='https://github.com/amake/twtrgrep',
    author='Aaron Madlon-Kay',
    author_email='aaron@madlon-kay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='twitter search grep',
    py_modules=['twtrgrep'],
    install_requires=['tweepy'],
    entry_points={
        'console_scripts': [
            'twtrgrep=twtrgrep:main',
        ],
    },

)
