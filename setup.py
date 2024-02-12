from glob import glob
import pathlib
from os.path import basename, splitext

import setuptools

setuptools.setup(
    name="confstore",
    version="0.1.0",
    author="Kristofer Hallin, Johannes Jeppsson",
    author_email="clixon-pyapi@8n1.se",
    description="Config store through git",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/SUNET/configuration-store",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache-2.0",
    python_requires=">=3.10",
    install_requires=["GitPython>=3.1.41"],
    entry_points={
        "console_scripts":
            ["confstore=confstore.cli.confstore:main"]
    }
)
