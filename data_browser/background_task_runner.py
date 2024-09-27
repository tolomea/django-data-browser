from ibl_dm_axd.data_reports.models import ReportTask, CompletedReport
from ibl_dm_axd.data_reports.tasks import run_background_report
from django.conf import settings


def fetch_related_report(username, model_name, fields, media):
    return ReportTask.objects.filter(
        report_name="model_browser_report",
        owner=username,
        platform__key="main",
        kwargs__model_name=model_name,
        kwargs__fields=fields,
    ).last()


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
    return run_background_report.delay(**data)
