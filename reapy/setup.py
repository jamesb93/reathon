from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="reapy",
    version="0.0.1",
    author="James Bradbury",
    url="https://github.com/jamesb93/reapy",
    license="GLPv3+",
    author_email="jamesbradbury93@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Construct REAPER projects in Python.",
    packages=find_packages()
)
