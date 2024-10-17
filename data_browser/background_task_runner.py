from django.conf import settings
from data_browser.helpers import DDBReportTask, ddb_run_background_report
from data_browser.models import ReportTask


def fetch_related_report(username, model_name, fields, media):
    report_name = model_name if DDBReportTask == ReportTask else "model_browser_report"
    filters = dict(
        report_name=report_name,
        owner=username,
        platform__key="main",
        kwargs__model_name=model_name,
        kwargs__fields=fields,
        kwargs__media=media,
    )
    return DDBReportTask.objects.filter(**filters).last()


def run_query(username, model_name, fields, media) -> str:
    data = {
        "report_name": "model_browser_report",
        "owner": username,
        "model_name": model_name,
        "fields": fields,
        "media": media,
        "platform": "main",
        "store_task": True,
        "sync_mode": settings.DEBUG,
    }
    return ddb_run_background_report.delay(**data)
