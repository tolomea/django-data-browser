import csv
import json

import data_browser.models
import pytest
from django.contrib.auth.models import User

from . import models

true = True
false = False
null = None


def dump(val):
    print(json.dumps(val, indent=4, sort_keys=True))


class ANY:  # pragma: no cover
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)


@pytest.fixture
def products(db):
    address = models.Address.objects.create(city="london")
    producer = models.Producer.objects.create(name="Bob", address=address)
    models.Product.objects.create(name="a", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="b", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="c", size=2, size_unit="g", producer=producer)


def test_query_html(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    context = json.loads(res.context["ctx"])
    context["config"]["version"] = "redacted"
    context["initialState"]["version"] = "redacted"
    snapshot.assert_match(context, "context")


def test_query_html_no_perms(admin_user, admin_client, snapshot):
    admin_user.is_superuser = False
    admin_user.save()
    res = admin_client.get("/data_browser/query//.html?")
    assert res.status_code == 200
    context = json.loads(res.context["ctx"])
    context["config"]["version"] = "redacted"
    context["initialState"]["version"] = "redacted"
    snapshot.assert_match(context, "context")


def test_query_ctx(admin_client, snapshot):
    res = admin_client.get("/data_browser/query//.ctx?")
    assert res.status_code == 200
    context = res.json()
    context["config"]["version"] = "redacted"
    context["initialState"]["version"] = "redacted"
    snapshot.assert_match(context, "context")
    with open("frontend/src/context_fixture.json", "w") as f:
        json.dump(context, f, indent=4, sort_keys=True)
        f.write("\n")


@pytest.mark.usefixtures("products")
def test_query_json_bad_fields(admin_client):
    res = admin_client.get(
        "".join(
            [
                "/data_browser/query/tests.Product/",
                "size-0,name+1,size_unit,bob-2,is_onsale,pooducer__name,producer__name.json",
                "?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx",
            ]
        )
    )
    assert res.status_code == 200
    assert json.loads(res.content.decode("utf-8"))["results"] == [
        [1, "a", "g", False, "Bob"],
        [1, "b", "g", False, "Bob"],
    ]


def test_query_html_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Bob/size-0,name+1,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_query_csv(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.csv?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    print(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    assert rows == [["size", "name", "size_unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]


@pytest.mark.usefixtures("products")
def test_query_json(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    data["version"] = "redacted"
    snapshot.assert_match(data, "data")


@pytest.mark.usefixtures("products")
def test_query_json_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Bob/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_csv(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="tests.Product",
        fields="size-0,name+1,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 200
    print(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    assert rows == [["size", "name", "size_unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]

    view.owner = User.objects.create(is_staff=True)
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_json(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="tests.Product",
        fields="size-0,name+1,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.pk}.json")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.json")
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    dump(data)
    assert data == {"results": [[1, "a", "g"], [1, "b", "g"]]}

    view.owner = User.objects.create(is_staff=True)
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 404
