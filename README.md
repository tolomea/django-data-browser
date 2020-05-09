# django-data-browser

Django app for user friendly querying of Django models

## installation

add 'data_browser` to installed_apps
path("data-browser/", include("data_browser.urls")),
migrate

## Development

The easiest way to develop this is against your existing client project.

The compiled Javascript is checked into the repo, so if only want to mess with the Python then it's sufficient to

1: Install data_browser in editable mode `pip install -e <directory to your git clone>`

If you want to modify the Javascript then you also need to

2: Enable proxying to the JS dev server by adding `DATA_BROWSER_DEV = True` to your settings
3: Run the dev server with `WDS_SOCKET_PORT=3000 PUBLIC_URL=data_browser npm start`
The WDS_SOCKET_PORT is so the proxied JS can find the webpack dev server.
The PUBLIC_URL tells the dev server what path to serve from and should be the same as the URL you have mounted the data-browser on in you urls.py file.

To build the JS, move the files around appropriately and recreate the wheels run `build.sh`
