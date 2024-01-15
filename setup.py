from glob import glob
from os.path import basename, splitext

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="augitlog",
    version="0.0.1",
    author="Kristofer Hallin, Johannes Jeppsson",
    author_email="clixon-pyapi@8n1.se",
    description="Audit log through git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SUNET/configuration-store",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
