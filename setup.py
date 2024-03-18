from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="abbacus",
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
)
