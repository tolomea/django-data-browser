#!/bin/bash
set -ex

(cd frontend; npm run build)

rm -Rf data_browser/fe_build
cp -a frontend/build data_browser/fe_build
mkdir -p data_browser/templates/data_browser
cp frontend/build/index.html data_browser/templates/data_browser/index.html
git add data_browser/fe_build data_browser/templates/data_browser/index.html

rm -Rf dist build
python -m pip install -U pip
python -m pip install --upgrade setuptools wheel twine check-manifest
check-manifest -v
python setup.py sdist bdist_wheel
twine check dist/*

set +x
echo SUCCESS
echo
echo git commit
echo git tag -a -m \"\" x.y.z
echo git push --tags
echo python -m twine upload -u __token__ dist/*
