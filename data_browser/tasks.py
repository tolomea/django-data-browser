from datetime import timedelta
from sys import getsizeof

import pandas as pd
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import QueryDict

from data_browser.models import CompletedReport, Platform, ReportState, ReportTask
from data_browser.query import Query
import traceback
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
    try:
        class MockRequest:
            def __init__(self, user):
                self.user = user
                self.data_browser = {"public_view": False, "fields": set(), "calculated_fields": set()}
                self.GET = QueryDict('', mutable=True)
                self.POST = QueryDict('', mutable=True)
                self.META = {}
                self.method = 'GET'

            def get_host(self):
                return 'localhost'

        from data_browser.common import set_global_state, GlobalState, _State, settings
        from data_browser.views import _data_response
        from data_browser.orm_admin import get_models

        User = get_user_model()
        user = User.objects.get(username=owner)
        mock_request = MockRequest(user)

        # Set up the global state
        global_state = GlobalState()
        global_state._state = _State(None, request=mock_request, public_view=False, set_ddb=True)
        global_state._state.models = get_models(mock_request)

        # Use set_global_state as a context manager
        with set_global_state(request=mock_request, public_view=False):
            query = Query.from_request(model_name, fields, params)
            response = _data_response(query, "json", privileged=True, raw=True, remove_limit=True)

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
    except Exception as e:
        task.state = ReportState.ERROR
        task.traceback = traceback.format_exc()
        task.save()