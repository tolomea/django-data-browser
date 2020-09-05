import csv
import json
from datetime import datetime

import django
import pytest
from django.contrib.auth.models import User
from django.utils import timezone

import data_browser.models

from .core import models
from .util import update_fe_fixture


def dump(val):
    print(json.dumps(val, indent=4, sort_keys=True))


@pytest.fixture
def products(db):
    address = models.Address.objects.create(city="london")
    producer = models.Producer.objects.create(name="Bob", address=address)
    models.Product.objects.create(name="a", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="b", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="c", size=2, size_unit="g", producer=producer)


@pytest.fixture
def pivot_products(db):
    address = models.Address.objects.create(city="london", street="bad")
    producer = models.Producer.objects.create(name="Bob", address=address)
    datetimes = [
        datetime(2020, 1, 1, tzinfo=timezone.utc),
        datetime(2020, 2, 1, tzinfo=timezone.utc),
        datetime(2020, 2, 2, tzinfo=timezone.utc),
        datetime(2021, 1, 1, tzinfo=timezone.utc),
        datetime(2021, 1, 2, tzinfo=timezone.utc),
        datetime(2021, 1, 3, tzinfo=timezone.utc),
    ]
    for i, dt in enumerate(datetimes):
        models.Product.objects.create(
            created_time=dt, name=str(dt), size=i + 1, producer=producer
        )


@pytest.mark.skipif(django.VERSION < (2, 2), reason="Django version 2.2 required")
def test_query_html(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    config = json.loads(res.context["config"])
    snapshot.assert_match(config, "config")


def test_query_query(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.query?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    query = json.loads(res.content.decode("utf-8"))
    snapshot.assert_match(query, "query")


@pytest.mark.skipif(django.VERSION < (2, 2), reason="Django version 2.2 required")
def test_query_html_no_perms(admin_user, admin_client, snapshot):
    admin_user.is_superuser = False
    admin_user.save()
    res = admin_client.get("/data_browser/query//.html?")
    assert res.status_code == 200
    config = json.loads(res.context["config"])
    snapshot.assert_match(config, "config")


@pytest.mark.skipif(django.VERSION < (2, 2), reason="Django version 2.2 required")
def test_query_ctx(admin_client, snapshot):
    res = admin_client.get("/data_browser/query//.ctx?")
    assert res.status_code == 200
    config = res.json()
    snapshot.assert_match(config, "config")
    update_fe_fixture("frontend/src/context_fixture.json", config)


@pytest.mark.usefixtures("products")
def test_query_json_bad_fields(admin_client):
    res = admin_client.get(
        "".join(
            [
                "/data_browser/query/core.Product/",
                "size-0,name+1,size_unit,bob-2,is_onsale,pooducer__name,producer__name.json",
                "?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx",
            ]
        )
    )
    assert res.status_code == 200
    assert json.loads(res.content.decode("utf-8"))["rows"] == [
        {
            "size": 1,
            "name": "a",
            "size_unit": "g",
            "is_onsale": False,
            "producer__name": "Bob",
        },
        {
            "size": 1,
            "name": "b",
            "size_unit": "g",
            "is_onsale": False,
            "producer__name": "Bob",
        },
    ]


def test_query_bad_media(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.bob?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_query_csv(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.csv?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    dump(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    assert rows == [["size", "name", "size_unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]


@pytest.mark.usefixtures("pivot_products")
def test_query_csv_pivoted(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Product/created_time__year+0,&created_time__month+1,id__count,size__max.csv?"
    )
    assert res.status_code == 200
    dump(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    assert rows == [
        ["created_time month", "January", "", "Feburary", ""],
        ["created_time year", "id count", "size max", "id count", "size max"],
        ["2020.0", "1.0", "1.0", "2.0", "3.0"],
        ["2021.0", "3.0", "6.0", "", ""],
    ]


testdata = [
    ("----"),
    ("---b"),
    ("--c-"),
    ("--cb"),
    ("-r--"),
    ("-r-b"),
    ("-rc-"),
    ("-rcb"),
    ("d---"),
    ("d--b"),
    ("d-c-"),
    ("d-cb"),
    ("dr--"),
    ("dr-b"),
    ("drc-"),
    ("drcb"),
]


@pytest.mark.usefixtures("pivot_products")
@pytest.mark.parametrize("key", testdata)
def test_query_csv_pivot_permutations(admin_client, key, snapshot):
    fields = []
    if "r" in key:
        fields.append("created_time__year+0")
    if "c" in key:
        fields.append("&created_time__month+1")
    if "b" in key:
        fields.extend(["id__count", "size__max"])
    filters = "" if "d" in key else "id__equals=-1"

    res = admin_client.get(
        f"/data_browser/query/core.Product/{','.join(fields)}.csv?{filters}"
    )
    assert res.status_code == 200
    dump(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    snapshot.assert_match(rows, "key")


@pytest.mark.usefixtures("products")
def test_query_json(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    snapshot.assert_match(data, "data")


@pytest.mark.usefixtures("pivot_products")
def test_query_json_pivot(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/core.Product/created_time__year+0,&created_time__month+1,id__count,size__max.json?"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    snapshot.assert_match(data, "data")


@pytest.mark.usefixtures("products")
def test_query_json_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Bob/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_csv(admin_client, settings):
    view = data_browser.models.View.objects.create(
        model_name="core.Product",
        fields="size-0,name+1,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 200
    dump(res.content.decode("utf-8"))
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    dump(rows)
    assert rows == [["size", "name", "size_unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]

    settings.DATA_BROWSER_ALLOW_PUBLIC = False
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 404
    settings.DATA_BROWSER_ALLOW_PUBLIC = True

    view.owner = User.objects.create(is_staff=True)
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_json(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="core.Product",
        fields="size-0,name+1,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    dump(data)
    assert data == {
        "rows": [
            {"size": 1, "name": "a", "size_unit": "g"},
            {"size": 1, "name": "b", "size_unit": "g"},
        ],
        "cols": [{}],
        "body": [[{}, {}]],
        "length": 2,
        "formatHints": {
            "name": {},
            "size": {
                "decimalPlaces": 0,
                "significantFigures": 3,
                "lowCutOff": 0.0001,
                "highCutOff": 1e10,
            },
            "size_unit": {},
        },
    }

    view.owner = User.objects.create(is_staff=True)
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 404
