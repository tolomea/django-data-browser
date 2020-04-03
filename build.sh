#!/bin/bash
(cd frontend; npm run build)
rm -Rf data_browser/static
cp -a frontend/build/static data_browser/static
cp frontend/build/index.html data_browser/templates/data_browser/index.html
pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
#python -m twine upload dist/*
