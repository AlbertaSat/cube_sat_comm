import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cubesatcomm",
    version="0.0.1",
    author="Brendan Gluth",
    author_email="gluthb@gmail.com",
    description="Simple terminal program to communicate with cube satelites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "result"
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
