#!/bin/bash
(cd frontend; npm run build)
rm -Rf data_browser/fe_build
cp -a frontend/build data_browser/fe_build
cp frontend/build/index.html data_browser/templates/data_browser/index.html
pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
#python -m twine upload dist/*
