import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="b3-cdi-curve",
    version="1.0.0",
    description="Create a local DB with the term structure of the Brazilian CDI curve (data from B3).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fluxonaut/b3_cdi_curve",
    author="Fluxonaut",
    author_email="contact@fluxonaut.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["b3cdi"],
    include_package_data=True,
    install_requires=[
        "beautifulsoup4>=4.9.3",
        "numpy>=1.19.2",
        "pandas>=1.1.3",
        "pylint>=2.6.0",
        "requests>=2.24.0",
        "html5lib>=1.1",
        "scipy>=1.5.3",
    ],
)