from setuptools import setup, find_packages

setup(
    name="entropy-calculator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "entropy-calculator = entropy_calculator.main:main",
        ]
    },
)
