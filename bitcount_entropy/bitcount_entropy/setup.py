from setuptools import setup, find_packages

setup(
    name='bitcount_entropy',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bitcount_entropy=bitcount_entropy.main:main',
        ],
    },
    install_requires=[
        'numpy',
    ],
)
