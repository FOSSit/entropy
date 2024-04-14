from setuptools import setup, find_packages

setup(
    name='entropy_calculator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'entropy_calculator=entropy_calculator.entropy:main'
        ]
    },
)
