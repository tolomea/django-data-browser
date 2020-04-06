# django-data-browser
Django app for user friendly querying of Django models


## Development

The easiest way to develop this is against your existing client project.

The compiled Javascript is checked into the repo, so if only want to mess with the Python then it's sufficient to

1: Install data_browser in editable mode `pip install -e <directory to your git clone>`

If you want to modify the Javascript then you also need to

2: Enable proxying to the JS dev server by adding `DATA_BROWSER_DEV = True` to your settings
3: Fix up paths on the JS side by changing `homepage` in package.json to the correct path e.g. `/data_browser/`

To build the JS and move the files around appropriately and recreate the wheels run `build.sh`
