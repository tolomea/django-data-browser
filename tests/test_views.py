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


@pytest.mark.parametrize("format", ["sql", "profile", "pstats", "profile_sql"])
def test_query_misc_formats(admin_client, format):
    # we're not going to check the result as they vary and it's sufficient that it doesn't blow up
    res = admin_client.get(
        f"/data_browser/query/core.Product/size-0,name+1,size_unit.{format}?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200


@pytest.mark.skipif(django.VERSION < (2, 1), reason="Django version 2.1 required")
def test_query_explain(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Product/size-0,name+1,size_unit.explain?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200


def test_query_sql_aggregate(admin_client):
    res = admin_client.get("/data_browser/query/core.Product/size__count.sql")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "format", ["bad", "profile_bad", "pstats_bad", "profilesql", "pstatsbad"]
)
def test_query_bad_formats(admin_client, format):
    res = admin_client.get(
        f"/data_browser/query/core.Product/size-0,name+1,size_unit.{format}?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


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
            "is_onsale": "False",
            "producer__name": "Bob",
        },
        {
            "size": 1,
            "name": "b",
            "size_unit": "g",
            "is_onsale": "False",
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
    res = res.getvalue().decode("utf-8")
    dump(res)
    rows = list(csv.reader(res.splitlines()))
    dump(rows)
    assert rows == [["Size", "Name", "Size unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]


@pytest.mark.usefixtures("pivot_products")
def test_query_csv_pivoted(admin_client):
    res = admin_client.get(
        "/data_browser/query/core.Product/created_time__year+0,&created_time__month+1,id__count,size__max.csv?"
    )
    assert res.status_code == 200
    res = res.getvalue().decode("utf-8")
    dump(res)
    rows = list(csv.reader(res.splitlines()))
    dump(rows)
    assert rows == [
        ["Created time month", "January", "", "Feburary", ""],
        ["Created time year", "ID count", "Size max", "ID count", "Size max"],
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
    res = res.getvalue().decode("utf-8")
    dump(res)
    rows = list(csv.reader(res.splitlines()))
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


@pytest.mark.usefixtures("products")
def test_query_is_null_date_filter(admin_client, snapshot):
    res = admin_client.get(
        "/data_browser/query/core.Product/name+0.json?created_time__is_null=NotNull"
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
    res = res.getvalue().decode("utf-8")
    dump(res)
    rows = list(csv.reader(res.splitlines()))
    dump(rows)
    assert rows == [["Size", "Name", "Size unit"], ["1.0", "a", "g"], ["1.0", "b", "g"]]

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
                "highCutOff": 10000000000.0,
                "lowCutOff": 0.0001,
                "maximumFractionDigits": 0,
                "minimumFractionDigits": 0,
                "significantFigures": 3,
            },
            "size_unit": {},
        },
    }

    view.owner = User.objects.create(is_staff=True)
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.csv")
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_bad_filter(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="core.Product",
        fields="size-0,name+1,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
        public=True,
    )

    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 200

    view.query = "sixe__lt=2&id__gt=0"
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 400

    view.query = "size__lx=2&id__gt=0"
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 400

    view.query = "size__lt=a&id__gt=0"
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.public_slug}.json")
    assert res.status_code == 400


@pytest.mark.usefixtures("products")
def test_action(admin_client):
    url = "/data_browser/query/core.Product/id.%s"

    ids = set(models.Product.objects.values_list("id", flat=True))
    assert len(ids) == 3

    # check our view is right
    res = admin_client.get(url % "json")
    assert {row["id"] for row in res.json()["rows"]} == ids

    # ask data browser for the action request
    res = admin_client.post(
        url % "html",
        {"action": "delete_selected", "field": "id"},
        content_type="application/json",
    ).json()
    assert res == {
        "method": "post",
        "url": "/admin/core/product/?",
        "data": [
            ["action", "delete_selected"],
            ["select_across", 0],
            ["index", 0],
            ["data_browser", 1],
            *[["_selected_action", id_] for id_ in ids],
        ],
    }

    # post action to changelist
    data = dict(res["data"])
    data["_selected_action"] = [int(id_) for id_ in ids]  # JS will format 1.0 as 1
    res = admin_client.post(res["url"], data)
    assert "Are you sure you want to delete the selected" in res.rendered_content
    assert set(res.context[0]["queryset"].values_list("id", flat=True)) == ids


@pytest.mark.usefixtures("products")
def test_action_filtered(admin_client):
    url = "/data_browser/query/core.Product/id.%s?size__equals=2"

    (id_,) = set(models.Product.objects.filter(size=2).values_list("id", flat=True))

    # check our view is right
    res = admin_client.get(url % "json")
    assert {row["id"] for row in res.json()["rows"]} == {id_}

    # ask data browser for the action request
    res = admin_client.post(
        url % "html",
        {"action": "delete_selected", "field": "id"},
        content_type="application/json",
    ).json()
    assert res == {
        "method": "post",
        "url": "/admin/core/product/?",
        "data": [
            ["action", "delete_selected"],
            ["select_across", 0],
            ["index", 0],
            ["data_browser", 1],
            ["_selected_action", id_],
        ],
    }

    # post action to changelist
    data = dict(res["data"])
    data["_selected_action"] = int(data["_selected_action"])  # JS will format 1.0 as 1
    res = admin_client.post(res["url"], data)
    assert "Are you sure you want to delete the selected" in res.rendered_content
    assert set(res.context[0]["queryset"].values_list("id", flat=True)) == {id_}


@pytest.mark.usefixtures("products")
def test_related_action(admin_client):
    url = "/data_browser/query/core.Product/address__id,producer__id,id.%s"

    product_ids = set(models.Product.objects.values_list("id", flat=True))
    assert len(product_ids) == 3

    (producer_id,) = set(models.Producer.objects.values_list("id", flat=True))

    # check our view is right
    res = admin_client.get(url % "json")
    assert {row["id"] for row in res.json()["rows"]} == product_ids
    assert {row["producer__id"] for row in res.json()["rows"]} == {producer_id}

    # ask data browser for the action request
    res = admin_client.post(
        url % "html",
        {"action": "delete_selected", "field": "producer__id"},
        content_type="application/json",
    ).json()
    assert res == {
        "method": "post",
        "url": "/admin/core/producer/?",
        "data": [
            ["action", "delete_selected"],
            ["select_across", 0],
            ["index", 0],
            ["data_browser", 1],
            ["_selected_action", producer_id],
        ],
    }

    # post action to changelist
    data = dict(res["data"])
    data["_selected_action"] = int(data["_selected_action"])  # JS will format 1.0 as 1
    res = admin_client.post(res["url"], data)
    assert "Are you sure you want to delete the selected" in res.rendered_content
    assert set(res.context[0]["queryset"].values_list("id", flat=True)) == {producer_id}
