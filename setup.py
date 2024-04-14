from setuptools import setup, find_packages

setup(
    name='entropy-calculator',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'entropy-calculator = entropy.calculator:main'
        ]
    },
    install_requires=[
        'numpy'
    ],
    author='Vinayak',
    description='Calculate byte-level or bit-level entropy of files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
