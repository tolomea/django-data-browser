#!/bin/bash
set -ex

git add README.rst data_browser/__init__.py
git update-index --refresh  # will error if there are unstaged changes

./build_fe.sh

git add data_browser/fe_build data_browser/templates/data_browser/index.html

./build_whl.sh

version=$(python -c "import data_browser; print(data_browser.version)")
set +x
echo SUCCESS
echo
echo "To release run the following:"
echo "    git commit -m $version && git tag -a -m $version $version && git push --follow-tags && python -m twine upload dist/*"
