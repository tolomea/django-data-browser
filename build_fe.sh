#!/bin/bash
set -ex

(cd frontend; npm run build)
rm -Rf data_browser/fe_build
cp -a frontend/build data_browser/fe_build
mkdir -p data_browser/templates/data_browser
cp frontend/build/index.html data_browser/templates/data_browser/index.html
