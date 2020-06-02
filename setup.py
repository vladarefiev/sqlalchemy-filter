import os
import re

from setuptools import find_packages, setup


path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(path, "sqlalchemy_filter", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open(os.path.join(path, "README.md"), encoding="utf-8") as f:
    readme = f.read()


setup(
    name="sqlalchemy-filter",
    version=version,
    packages=find_packages(exclude=["tests*"]),
    install_requires=["sqlalchemy"],
    author="Vlad Arefev",
    author_email="vlad.arefiev1992@gmail.com",
    url="https://github.com/vladarefiev/sqlalchemy-filter",
    description=(
        "sqlalchemy-filter is a helper library to perform filtering over sqlalchemy queries"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Database :: Front-Ends",
        "Typing :: Typed",
    ],
    license="BSD",
)
