"""AoC GraphQL setup."""
from setuptools import setup, find_packages

setup(
    name='aocgql',
    version='2.0.0',
    description='Age of Empires II graphql interface.',
    url='https://github.com/siegeengineers/aoc-graphql/',
    license='MIT',
    author='happyleaves',
    author_email='happyleaves.tfr@gmail.com',
    packages=find_packages(),
    install_requires=[
        'coloredlogs>=10.0',
        'boto3>=1.9.243',
        'dateparser>=0.7.1',
        'Flask>=1.0.2',
        'Flask-Caching>=1.7.2',
        'Flask-Cors>=3.0.7',
        'Flask-GraphQL==2.0.0',
        'graphene>=2.1.8',
        'graphene-sqlalchemy>=2.2.2',
        'mgzdb>=1.2.5',
        'networkx>=2.2',
        'psycopg2-binary>=2.8.3'
    ],
    entry_points = {
        'console_scripts': ['aocgql=aocgql.__main__:setup'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
