from .admin import AddressAdmin, ProductAdmin
from .models import Address, Producer, Product


class TestAnnotationOptimization:
    def test_annotation_loaded_on_detail(self, admin_client, mocker):
        get_queryset = mocker.patch(
            "tests.admin.AddressAdmin.andrew.get_queryset",
            wraps=AddressAdmin.andrew.get_queryset,
        )
        a = Address.objects.create()
        assert (
            admin_client.get(f"/admin/tests/address/{a.pk}/change/").status_code == 200
        )
        get_queryset.assert_called_once()

    def test_annotation_loaded_unnecessarily_on_detail(self, admin_client, mocker):
        get_queryset = mocker.patch(
            "tests.admin.ProductAdmin.annotated.get_queryset",
            wraps=ProductAdmin.annotated.get_queryset,
        )
        p = Product.objects.create(producer=Producer.objects.create())
        assert (
            admin_client.get(f"/admin/tests/product/{p.pk}/change/").status_code == 200
        )
        get_queryset.assert_called_once()

    def test_annotation_loaded_on_list(self, admin_client, mocker):
        get_queryset = mocker.patch(
            "tests.admin.ProductAdmin.annotated.get_queryset",
            wraps=ProductAdmin.annotated.get_queryset,
        )
        assert admin_client.get(f"/admin/tests/product/").status_code == 200
        get_queryset.assert_called_once()

    def test_annotation_not_loaded_on_list(self, admin_client, mocker):
        get_queryset = mocker.patch(
            "tests.admin.AddressAdmin.andrew.get_queryset",
            wraps=AddressAdmin.andrew.get_queryset,
        )
        assert admin_client.get(f"/admin/tests/address/").status_code == 200
        get_queryset.assert_not_called()
