import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


data_files = []
for directory in "data_browser/fe_build", "data_browser/templates":
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            data_files.append(os.path.join("..", path, filename))


setuptools.setup(
    name="django-data-browser",
    version="0.0.4",
    author="Gordon Wrigley",
    author_email="gordon.wrigley@gmail.com",
    description="git@github.com:tolomea/django-data-browser.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tolomea/django-data-browser",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    package_data={"": data_files},
)
