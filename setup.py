from setuptools import setup, find_packages

setup(
    name="kartr",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kartr=kartr.__main__:main',
        ],
    },
)
