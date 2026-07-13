from setuptools import setup, find_packages

setup(
    name="telegram-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "python-telegram-bot==20.7",
        "requests==2.31.0",
    ],
    python_requires=">=3.8",
)