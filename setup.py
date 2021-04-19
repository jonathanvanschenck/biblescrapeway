from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='biblescrapeway',
    version='0.1',
    author="Jonathan D B Van Schenck",
    author_email="vanschej@oregonstate.edu",
    description='A tool for scraping bible verses from the web',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanschenck/biblescrapeway",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bsw=biblescrapeway.cli:scrap
    ''',
)
