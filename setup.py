from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = [x.split('==')[0] for x in f.readlines()]

setup(
    name='shoutedfm',
    version='1.0.0',
    description='REST API of ShoutedFM streams live sessions schedule.',
    long_description=long_description,
    url='https://github.com/JonathanHuot/shoutedfm',
    author='Jonathan Huot',
    author_email='jonathan.huot@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='audio stream house music',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    install_requires=requires,
    entry_points={
        'console_scripts': [
            'shoutedfm=runserver:main',
        ],
    },
)
