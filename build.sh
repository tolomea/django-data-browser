#!/bin/bash
set -ex

./build_fe.sh
./build_whl.sh

git add data_browser/fe_build data_browser/templates/data_browser/index.html README.rst data_browser/__init__.py
version=$(python -c "import data_browser; print(data_browser.version)")
set +x
echo SUCCESS
echo
echo "To release run the following:"
echo "    git commit -m $version"
echo "    git tag -a -m $version $version"
echo "    git push --follow-tags"
echo "    python -m twine upload -u __token__ dist/*"
