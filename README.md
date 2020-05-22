# Interactive and user friendly querying of Django project DBs.

![screenshot](https://raw.githubusercontent.com/tolomea/django-data-browser/master/screenshot.png)

### Features

-   Zero config, if it's in the admin it's in the browser
-   Select fields (including calculated fields), aggregate, filter and sort
-   Automatically follow OneToOneFields and ForeignKeys
-   Respects per user admin permissions
-   Share views by URL
-   Save views and optionally make them available to services like Google sheets
-   Download views as CSV or JSON

### Roadmap (in no particular order)

-   ToMany support
-   Advanced filtering
-   PII controls
-   Graphs
-   Pivoting

## Demo

There is a live demo site available. The Django project is a small e-commerce site selling microservices.

Source: https://github.com/tolomea/data-browser-demo

Admin: https://data-browser-demo.herokuapp.com/admin/

Data Browser: https://data-browser-demo.herokuapp.com/data-browser/

Becuase it's hosted on Heroku free tier it might take a while to respond to the first page load.

## Installation

1. Run `pip install django-data-browser`
1. Add `"data_browser"` to installed_apps.
1. Add `path("data-browser/", include("data_browser.urls"))` to your urls.
1. Run `python manage.py migrate`.

## Security

There are two types of views in the Data Browser.

Query views support general querying of the database (checked against the users admin permissions) but can only be accessed by Django "staff members".

Saved Views can be accessed by anyone but they can only be used to access a view that has been saved and made public and they have long random URL's.

You can use the admin permission `data_browser | view | Can make a saved view publically available` to restrict who can make views public. To be public the view must be marked as public and owned by someone who has the permission. Users without the permission can not mark views as public and can not edit any view that is marked public.

## Sentry

The frontend code has builtin Sentry support, it is **disabled by default**. To enable it set the Django settings value `DATA_BROWSER_FE_DSN`, for example to set it to the Data Browser project Sentry use:

```
DATA_BROWSER_FE_DSN = "https://af64f22b81994a0e93b82a32add8cb2b@o390136.ingest.sentry.io/5231151"
```

## Customization and Performance

For concrete fields (as oppose to calculated ones) the Data Browser will do appropriate select and prefetch related calls to minimise it's database impact.

The Data Browser calls the normal admin `get_queryset` functions. You can use these to customize querysets as needed.

If necessary you can test to see if the databrowser is making the call as follows:

```
if request.databrowser:
    # Data Browser specific customization
```

This is particularly useful if you want to route the Data Browser to a DB replica.

The Data Browser also calls `get_fieldsets` to find out what fields the current user can access. When it does this it always passes a newly constructed instance of the relevant model. This is necessary to work around Django's User admin messing with the fieldsets when `None` is passed.

## Development

The easiest way to develop this is against your existing client project.

The compiled Javascript is checked into the repo, so if only want to mess with the Python then it's sufficient to:

1. Install the Data Browser in editable mode `pip install -e <directory to your git clone>`.

If you want to modify the Javascript then you also need to:

2. Enable proxying to the JS dev server by adding `DATA_BROWSER_DEV = True` to your settings.
3. Run the Javascript dev server with `WDS_SOCKET_PORT=3000 PUBLIC_URL=data_browser npm start`.
   The `WDS_SOCKET_PORT` is so the proxied JS can find it's dev server.
   The `PUBLIC_URL` tells the JS dev server what path to serve from and should be the same as the URL you have mounted the Data Browser on in you urls file.

To run the Python tests, in the top level of you git clone run `pip install -r requirements.txt` then `pytest`.

There is also pre-commit config for lint etc to enable this run `pip install pre-commit && pre-commit install` then lint will run on `git commit`. The linting includes Black and isort autoformatting.

To build the JS, move the files around appropriately and recreate the wheels run `build.sh`.

During development it can be useful to look at the `.ctx` and `.json` views. The `.ctx` view will show you the initial context being passed to the Javascript on page load. The `.json` view is the actual API request the Javascript uses to fetch query results.

### Structure

![structure](https://raw.githubusercontent.com/tolomea/django-data-browser/master/structure.svg)

### Naming

| Name        | Meaning                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| bound query | A query that has been validated against the config.                                                       |
| config      | Information that doesn't change based on the particular query, includes all the models and their fields.  |
| field name  | Just the name of the field e.g. `created_time`.                                                           |
| field path  | Includes information on how to reach the model the field is on e.g. `order__seller__created_time`.        |
| model name  | Fullstop seperated app and model names e.g. `myapp.MyModel`.                                              |
| model       | In Python the actual model class, in Javascript the model name as above.                                  |
| query       | The information that changes with the query being done, in the Javascript this also includes the results. |
| view        | A saved query.                                                                                            |

### Release History

| Version   | Date           | Summary               |
| --------- | -------------- | --------------------- |
| 1.1.2     | 2020-05-22     | Small fixes           |
| 1.1.1     | 2020-05-20     | Small fixes           |
| **1.1.0** | **2020-05-20** | **Aggregate support** |
| **1.0.2** | **2020-05-17** | **Py3.6 support**     |
| 1.0.1     | 2020-05-17     | Small fixes           |
| 1.0.0     | 2020-05-17     | Initial version       |
