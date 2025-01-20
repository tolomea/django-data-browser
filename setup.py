import os
from pathlib import Path

import setuptools

from data_browser import version

root = Path("data_browser")
data_files = []
for directory in ("templates", "web_root", "static"):
    for path, _, filenames in os.walk(root / directory):
        for filename in filenames:
            data_files.append(os.path.join("..", path, filename))


setuptools.setup(
    name="django-data-browser",
    version=version,
    author="IBL",
    author_email="developer@ibleducation.com",
    description="Interactive user-friendly database explorer.",
    long_description=Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    url="https://github.com/iblai/ibl-django-data-browser-app",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={"": data_files},
    install_requires=["Django>=3.2", "hyperlink", "python-dateutil", "sqlparse", "ipdb", "ipython", "pandas"],
    entry_points={
        "lms.djangoapp": [
            "data_browser = data_browser.apps:DataBrowserConfig",
        ],
        "cms.djangoapp": [
            "data_browser = data_browser.apps:DataBrowserConfig",
        ],
    },
)
