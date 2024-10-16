from datetime import timedelta
from sys import getsizeof

import pandas as pd
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from data_browser.models import CompletedReport, Platform, ReportState, ReportTask
from data_browser.query import Query

import logging

log = logging.getLogger(__name__)


@shared_task(bind=True)
def run_background_report(self, **kwargs):
    task_id = self.request.id
    kwargs["task_id"] = task_id

    params = kwargs.get("params", {})
    model_name = kwargs.get("model_name")
    fields = kwargs.get("fields")
    owner = kwargs.get("owner")
    platform = Platform.objects.get(key=kwargs.get("platform"))
    task = ReportTask.objects.create(
        report_name=model_name,
        platform=platform,
        owner=owner,
        generator="db_browser",
        background_task_id=task_id,
        kwargs=kwargs,
    )
    query = Query.from_request(model_name, fields, params)

    from data_browser.views import _data_response
    response = _data_response(
        query, "json", privileged=True, raw=True, remove_limit=True
    )

    now = timezone.now()
    completed_report = CompletedReport.objects.create(
        task=task,
        created_on=now,
        content=pd.DataFrame(response).to_dict(orient="split"),
        expires_on=now + timedelta(seconds=settings.REPORT_EXPIRY_SECONDS),
    )
    task.stopped = now
    task.state = ReportState.COMPLETED
    task.save()
    log.info(f"Report stored size: {getsizeof(completed_report.content)} bytes")
