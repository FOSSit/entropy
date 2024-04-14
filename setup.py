from setuptools import setup

setup(
    name='entropy-calculator',
    version='0.1',
    py_modules=['your_script'],
    install_requires=[
        'numpy',
    ],
    entry_points='''
        [console_scripts]
        entropy-calculator=your_script:main
    '''
)