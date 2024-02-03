import hyperlink
from django.db import models
from django.urls import reverse
from django.utils import crypto
from django.utils import timezone

from data_browser.common import PUBLIC_PERM
from data_browser.common import SHARE_PERM
from data_browser.common import global_state
from data_browser.common import has_permission
from data_browser.common import set_global_state
from data_browser.common import settings


def get_id():
    return crypto.get_random_string(length=12)


class View(models.Model):
    class Meta:
        permissions = [
            (PUBLIC_PERM, "Can make a saved view publicly available"),
            (SHARE_PERM, "Can share a saved view with other users"),
        ]

    id = models.CharField(primary_key=True, max_length=12, default=get_id)
    created_time = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=64, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    public = models.BooleanField(default=False)
    public_slug = models.CharField(max_length=12, default=get_id, blank=False)
    shared = models.BooleanField(default=False)

    model_name = models.CharField(max_length=64, blank=False)
    fields = models.TextField(blank=True)
    query = models.TextField(blank=True)
    limit = models.IntegerField(blank=False, null=False, default=1000)

    def get_query(self):
        from data_browser.query import Query

        params = list(hyperlink.parse(f"?{self.query}").query)
        params.append(("limit", str(self.limit)))
        return Query.from_request(self.model_name, self.fields, params)

    @property
    def url(self):
        return self.get_query().get_full_url("html")

    def _public_url(self, fmt):
        with set_global_state(user=self.owner, public_view=True):
            if not (has_permission(self.owner, PUBLIC_PERM) and self.public):
                return "N/A"

            if not settings.DATA_BROWSER_ALLOW_PUBLIC:
                return "Public Views are disabled in Django settings."

            if not self.is_valid():
                return "View is invalid"

            url = reverse(
                "data_browser:view", kwargs={"pk": self.public_slug, "media": "csv"}
            )
            url = global_state.request.build_absolute_uri(url)

            return fmt.format(url=url)

    def public_link(self):
        return self._public_url("{url}")

    def google_sheets_formula(self):
        return self._public_url('=importdata("{url}")')

    def __str__(self):
        return f"{self.model_name} view: {self.name}"

    def is_valid(self):
        return self.get_query().is_valid(global_state.models)
