from setuptools import setup, find_packages

setup(
    name="EaseUI",
    version="0.1",
    packages=find_packages(),
    description="A Python library for rapid UI prototyping",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="PainDe0Mie",
    author_email="painde0mie@gmail.com",
    url="http://github.com/PainDe0Mie/easeui",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "pillow",
        "tkhtmlview",
        "matplotlib.pyplot"
    ],
)