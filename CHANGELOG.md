## Unreleased

## 0.0.4
- Add edX plugin support 
- Ensures report detail can be viewed
- UI Improvements. Adds icons for actions

## 0.0.3
- UI Improvements

## 0.0.2
- Ensure we can choose custom models and functions 
  * Defaults are
  ```
    "DATA_BROWSER_REPORT_TASK_MODEL": "data_browser.models.ReportTask",
      "DATA_BROWSER_REPORT_STATE_MODEL": "data_browser.models.ReportState",
      "DATA_BROWSER_RUN_BACKGROUND_REPORT_FUNC": "data_browser.tasks.run_background_report",
      "DATA_BROWSER_GENERATION_TIMELINE_SECONDS": 300,
      "REPORT_EXPIRY_SECONDS": 86400,
    ```

- Ensure static files arw available in django format
- Ensure background tasks run in celery process

## 0.0.1
- Adds background report support