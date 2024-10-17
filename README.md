## IBL Django Data Browser App

Installation
------------

1. Run ``pip install django-data-browser``.
2. Add ``"data_browser"`` to installed_apps.
3. Add ``path("admin/data-browser/", include("data_browser.urls"))`` to your urls.
4. Run ``python manage.py migrate``.
5. If you have queryset annotations in your admin or are interested in exposing calculated values see the `Calculated and Annotated fields`_ section.

Development
------------
1. Clone the repository
2. Install in editable install mode `pip install -e <dir>`
3. Run NPM for frontend files. 
```
cd frontend 
npm install
```

Customizing the UI
------------
Front end files are in `frontend/`. When you make changes to any files, the files should be compiled using

`./build_fe.sh`

Background Tasks
------------
Full rows are automatically sent as background tasks and available for download once completed. The status can be viewed 
in `/axd_data_reports/reporttask/`

Additional configs
------------
In order to define a custom model class to store background reports into, you can specify it with the following configs

```
{
... other data browser configs...
        "DATA_BROWSER_REPORT_TASK_MODEL": "data_browser.models.ReportTask",
        "DATA_BROWSER_REPORT_STATE_MODEL": "data_browser.models.ReportState",
        "DATA_BROWSER_RUN_BACKGROUND_REPORT_FUNC": "data_browser.tasks.run_background_report",
        "DATA_BROWSER_GENERATION_TIMELINE_SECONDS": 300,
        "REPORT_EXPIRY_SECONDS": 86400,
        
}
```

