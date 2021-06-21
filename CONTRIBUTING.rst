****************************************************************
Useful information for contributors.
****************************************************************

.. contents::
    :depth: 1


Roadmap (in no particular order)
*********************************

* UI improvements
* Graphs
* And/Or filtering
* User specified calculated fields
* Comparing to other fields
* Scheduled views
* Totals


Two audiences
*************************

There are two Data Browser user bases with differing need which must both be accommodated.

The developers who install the Data Browser into Django sites are crucial to adoption.
For this group it must be easy to install and configure, flexible and secure.
It is for this group that I'm willing to entertain stuff like rebranding, ideally people would stick with the default branding but if someone doesn't install it because they can't change the branding that's an adoption loss.
It is also for this group that the URL's and JSON files use machine readable names.

But the actual end user base is non technical business people.
These are people who should not need to know that ``Q(bob__fred=None)`` and ``Q(bob__fred__isnull=True)`` don't always return the same result when ``bob`` is a JSON field. For this group I would "fix" something like this even though it known and documented Django behavior.
It's also for this group that the frontend and CSV files both use human friendly names.


URL Format
*************************

The query URL format is ``query/<model>/<fields>.<format>?<filters>``.

Model is a Django app and model name for example ``library.Book``

Fields are a series of comma separated fields, where each field is the path to that field from the model with the parts separated by ``__``, e.g. ``author__name``. This path structure also includes aggregates and functions e.g. ``author__birthday__month__count``. Fields can be pivoted (where appropriate) by prefixing them with ``&``. And sorted by suffixing with a direction ``+``/``-`` and a priority e.g. ``author__birthday+1``.

Filters use the same ``__`` path format as fields including a lookup e.g. ``author__name__contains=Joe``.
Since filters always have a field and a lookup they always contain at least one ``__``.
Filters that don't contain a ``__`` are reserved, at the time of writing the only such filter is the row limit filter ``limit``.

Format determines the returned data format, the currently available formats are:

+---------+--------------------------------------------------------------------------------------------------+
| Format  | Details                                                                                          |
+=========+==================================================================================================+
| html    | Load the interactive JavaScript frontend.                                                        |
+---------+--------------------------------------------------------------------------------------------------+
| csv     | Standard CSV format.                                                                             |
+---------+--------------------------------------------------------------------------------------------------+
| json    | Standard JSON format, the JS frontend uses this for all data access.                             |
+---------+--------------------------------------------------------------------------------------------------+
| ctx     | See the JSON encoded config passed to the JS on page load.                                       |
+---------+--------------------------------------------------------------------------------------------------+
| query   | See the parsed URL in JSON format, the JS frontend uses this to bootstrap.                       |
+---------+--------------------------------------------------------------------------------------------------+
| qs      | | See the Django queryset.                                                                       |
|         | | This shows the primary query, pages with pivoted or calculated data may do additional queries. |
+---------+--------------------------------------------------------------------------------------------------+
| sql     | | See the raw SQL query that Django will perform.                                                |
|         | | This shows the primary query, pages with pivoted or calculated data may do additional queries. |
+---------+--------------------------------------------------------------------------------------------------+
| explain | | See the database explain output.                                                               |
|         | | This shows the primary query, pages with pivoted or calculated data may do additional queries. |
+---------+--------------------------------------------------------------------------------------------------+
| profile | | Run within cProfile and return the profile summary.                                            |
|         | | When suffixed with _csv (etc) will profile that specific format, defaults to JSON.             |
+---------+--------------------------------------------------------------------------------------------------+
| pstats  | | Run within cProfile and return the pstats file.                                                |
|         | | When suffixed with _csv (etc) will profile that specific format, defaults to JSON.             |
|         | | FYI these files are highly platform specific as they use Marshal internally.                   |
+---------+--------------------------------------------------------------------------------------------------+


Development
*************************

The easiest way to develop this is against your existing client project.

The compiled JavaScript is checked into the repo, so if only want to mess with the Python then it's sufficient to:

1. Install the Data Browser in editable mode ``pip install -e <directory to your git clone>``.

If you want to modify the JavaScript then you also need to:

2. Enable proxying to the JS dev server by adding ``DATA_BROWSER_DEV = True`` to your settings.
3. Run the JavaScript dev server with ``WDS_SOCKET_PORT=3000 PUBLIC_URL=data_browser npm start``.
   The ``WDS_SOCKET_PORT`` is so the proxied JS can find it's dev server.
   The ``PUBLIC_URL`` tells the JS dev server what path to serve from and should be the same as the URL you have mounted the Data Browser on in your urls file.

To run the Python tests, in the top level of your git clone run ``pip install -r requirements.txt`` then ``pytest``.

There is also pre-commit config for lint etc to enable this run ``pip install pre-commit && pre-commit install`` then lint will run on ``git commit``. The linting includes Black and isort autoformatting.

To build the JS, move the files around appropriately and recreate the wheels run ``build.sh``.

During development it can be useful to look at the ``.ctx`` and ``.json`` views. The ``.ctx`` view will show you the initial context being passed to the JavaScript on page load. The ``.json`` view is the actual API request the JavaScript uses to fetch query results.

Test model migrations
########################################

If you need to update the test model migrations delete the whole migration directory and run tests with the default sqlite config, this will generate new migrations.


Structure
########################################

.. image:: https://raw.githubusercontent.com/tolomea/django-data-browser/master/structure.svg
    :alt: structure
    :align: center


Terminology
########################################

+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Term             | Meaning                                                                                                                                    |
+==================+============================================================================================================================================+
| aggregate        | Corresponds to a Django aggregation function.                                                                                              |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| bound query      | A query that has been validated against the config.                                                                                        |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| calculated field | A field that can not be sorted or filtered, generally a field whose value comes from a property or function on the Admin or Model.         |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| concrete field   | A field that can be sorted and filtered, generally anything that came directly from the ORM.                                               |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| config           | Information that doesn't change based on the particular query, includes all the models and their fields.                                   |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| field name       | Just the name of the field e.g. ``created_time``.                                                                                          |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| field path       | Includes information on how to reach the model the field is on e.g. ``["order","seller","created_time"]``.                                 |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| function         | Corresponds to a Django database function for transforming a value, e.g. ``ExtractYear``.                                                  |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| model name       | Fullstop separated app and model names e.g. ``myapp.MyModel``, also includes synthetic 'models' for hosting aggregate and function fields. |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| model path       | Like field path for the model the field is on.                                                                                             |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| model            | In Python the actual model class, in JavaScript the model name as above.                                                                   |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| pretty...        | User friendly field, and path values                                                                                                       |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| query            | The information that changes with the query being done, in the JavaScript this also includes the results.                                  |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| type             | A data type, like string or number                                                                                                         |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| view             | A saved query.                                                                                                                             |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------------+

Most of the code deals with "models" that have "fields" that have "types".
In this context a "model" is just anything which might have fields.
An important consequence of this is that most types also have associated models which hold that types aggregate and function fields.
The special meanings of foreignkeys, aggregates, functions and calculated fields is confined to ``orm.py`` and ``orm_fields.py``.


Fields have 5 main properties.
########################################

+-----------+-----------------------------------------------------------------------------------------------+
| Property  | Meaning and impact                                                                            |
+===========+===============================================================================================+
| name      | The only required one.                                                                        |
+-----------+-----------------------------------------------------------------------------------------------+
| type      | If set then this field can be added to a query and will return results of the specified type. |
+-----------+-----------------------------------------------------------------------------------------------+
| concrete  | Can this field be sorted and filtered. Requires type to be set.                               |
+-----------+-----------------------------------------------------------------------------------------------+
| can_pivot | The field goes on the outside of a pivot table and as such can be pivoted.                    |
+-----------+-----------------------------------------------------------------------------------------------+
| model     | If set then this field has additional nested fields that are detailed on the given model.     |
+-----------+-----------------------------------------------------------------------------------------------+
