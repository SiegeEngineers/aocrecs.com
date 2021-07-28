"""aocrecs.com Setup."""
from setuptools import setup, find_packages

setup(
    name='aocrecs',
    version='4.0.4',
    description='aocrecs.com API.',
    url='https://github.com/siegeengineers/aocrecs.com/',
    license='MIT',
    author='happyleaves',
    author_email='happyleaves.tfr@gmail.com',
    packages=find_packages(),
    install_requires=[
        'aiocache==0.11.1',
        'aiodataloader==0.2.0',
        'aioify==0.3.2',
        'ariadne==0.11.0',
        'asyncpg==0.20.1',
        'boto3==1.10.46',
        'coloredlogs==10.0',
        'databases==0.3.2',
        'mgzdb>=1.4.4',
        'networkx==2.4',
        'python-dateutil==2.8.1',
        'python-multipart==0.0.5',
        'starlette==0.13.4',
        'uvicorn==0.11.7'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
