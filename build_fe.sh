#!/bin/bash
set -ex

(cd frontend; npm run build)
STATIC_PATH=data_browser/static/data_browser/
TEMPLATE_PATH=data_browser/templates/data_browser/

rm -Rf $STATIC_PATH/static
rsync -av --exclude='*.html'  frontend/build/* $STATIC_PATH
mkdir -p $TEMPLATE_PATH
cp frontend/build/index.html $TEMPLATE_PATH/index.html
rm -Rf frontend/build/
git add $STATIC_PATH $TEMPLATE_PATH