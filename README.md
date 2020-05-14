# django-data-browser

Django app for user friendly querying of Django models.

### Features

-   Select fields (including calculated fields), sort and fitler
-   Automatically follow OneToOneFields and ForeignKeys
-   Zero config, if it's in the admin it's in the browser
-   Respects per user admin permissions
-   Share views by URL
-   Save views and optionally make them available to services like Google sheets
-   Download views as CSV or JSON

### Roadmap (in no particular order)

-   ManyToMany and aggregation support
-   Advanced filtering
-   PII controls
-   Graphs
-   Pivoting

## Demo

There is a live demo site available. The Django project is a small e-commerce site selling microservices.

You can access the admin here https://data-browser-demo.herokuapp.com/admin/ and the Data Browser here https://data-browser-demo.herokuapp.com/data-browser/

Becuase it's hosted on Heroku free tier it might take up to 30 seconds to respond to the first page load.

## Installation

1. Run `pip install django-data-browser`
1. Add `"data_browser"` to installed_apps.
1. Add `path("data-browser/", include("data_browser.urls"))` to your urls.
1. Run `python manage.py migrate`.

## Security

There are two types of views in the Data Browser.

Query views support general querying of the database (checked against the users admin permissions) but can only be accessed by Django "staff members".

Saved Views can be accessed by anyone but they can only be used to access a view that has been saved and made public and have long random URL's. You can use admin permissions to restrict who can save views.

## Sentry

The frontend code has builtin Sentry support, it is **disabled by default**. To enable it set the Django settings value `DATA_BROWSER_FE_DSN`, for example to set it to the Data Browser project Sentry use:

```
DATA_BROWSER_FE_DSN = "https://af64f22b81994a0e93b82a32add8cb2b@o390136.ingest.sentry.io/5231151"
```

## Customization and Performance

For concrete fields (as oppose to calculated ones) the Data Browser will do appropriate select and prefetch related calls to minimise it's database impact.

The data-browser calls the normal admin `get_queryset` functions. You can use these to customize querysets as needed.

If necessary you can test to see if the databrowser is making the call as follows:

```
if request.databrowser:
	# Data Browser specific customization
```

This is particularly useful if you want to route the Data Browser to a DB replica.

The Data Browser also calls get_fieldsets to find out what fields the current user can access. When it does this it always passes a newly constructed instance of the relevant model. This is necessary to work around Django's User admin messing with the fieldsets when `None` is passed.

## Development

The easiest way to develop this is against your existing client project.

The compiled Javascript is checked into the repo, so if only want to mess with the Python then it's sufficient to:

1. Install data_browser in editable mode `pip install -e <directory to your git clone>`.

If you want to modify the Javascript then you also need to:

2. Enable proxying to the JS dev server by adding `DATA_BROWSER_DEV = True` to your settings.
3. Run the dev server with `WDS_SOCKET_PORT=3000 PUBLIC_URL=data_browser npm start`.
   The `WDS_SOCKET_PORT` is so the proxied JS can find the webpack dev server.
   The `PUBLIC_URL` tells the webpack dev server what path to serve from and should be the same as the URL you have mounted the data-browser on in you urls file.

To build the JS, move the files around appropriately and recreate the wheels run `build.sh`.

### Naming

field name,path

model, model_name

js vs python

### Architecture

include ctx

Diagram of parts
