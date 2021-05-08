from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='biblescrapeway',
    version='0.1.3',
    author="Jonathan D B Van Schenck",
    author_email="vanschej@oregonstate.edu",
    description='A tool for scraping bible verses from the web',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanschenck/biblescrapeway",
    packages=["biblescrapeway"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'Click',
        'beautifulsoup4',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        bsw=biblescrapeway.cli:scrap
    ''',
)
