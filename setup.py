from setuptools import setup

setup(
    name='entropy',
    version='0.1',
    py_modules=['entropy'],
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'entropy=entropy:main',
        ],
    },
)
