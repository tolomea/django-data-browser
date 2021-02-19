import os
from pathlib import Path

import setuptools

from data_browser import version

root = Path("data_browser")
data_files = []
for directory in ("fe_build", "templates", "web_root"):
    for (path, _, filenames) in os.walk(root / directory):
        for filename in filenames:
            data_files.append(os.path.join("..", path, filename))


setuptools.setup(
    name="django-data-browser",
    version=version,
    author="Gordon Wrigley",
    author_email="gordon.wrigley@gmail.com",
    description=(
        "A Django app for interactive user friendly browsing "
        "of a Django project DBs."
    ),
    long_description=Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    url="https://github.com/tolomea/django-data-browser",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={"": data_files},
    install_requires=[
        "Django>=2.2",
        "hyperlink",
        "python-dateutil",
        "sqlparse",
        'dataclasses; python_version<"3.7"',
    ],
)
