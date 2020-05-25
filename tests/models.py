from django.db import models
from django.utils import timezone

# models for perm testing


class InAdmin(models.Model):
    name = models.TextField()


class NotInAdmin(models.Model):
    name = models.TextField()


class InlineAdmin(models.Model):
    name = models.TextField()
    in_admin = models.ForeignKey(InAdmin, on_delete=models.CASCADE)


class Normal(models.Model):
    name = models.TextField()
    in_admin = models.ForeignKey(InAdmin, on_delete=models.CASCADE)
    not_in_admin = models.ForeignKey(NotInAdmin, on_delete=models.CASCADE)
    inline_admin = models.ForeignKey(InlineAdmin, on_delete=models.CASCADE)


# general models


class Tag(models.Model):
    name = models.TextField()


class Address(models.Model):
    city = models.TextField()
    street = models.TextField()

    def fred(self):
        assert self.street != "bad", self.street
        return "fred"

    @property
    def tom(self):
        assert self.street != "bad", self.street
        return "tom"


class Producer(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    name = models.TextField()


class Product(models.Model):
    name = models.TextField()
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    size = models.IntegerField()
    size_unit = models.TextField()
    default_sku = models.ForeignKey("SKU", null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    onsale = models.BooleanField(null=True)
    image = models.FileField()
    created_time = models.DateTimeField(default=timezone.now)
    only_in_list_view = models.TextField()

    not_in_admin = models.TextField()
    fk_not_in_admin = models.ForeignKey(InAdmin, null=True, on_delete=models.CASCADE)
    model_not_in_admin = models.ForeignKey(
        NotInAdmin, null=True, on_delete=models.CASCADE
    )

    def is_onsale(self):
        return False


class SKU(models.Model):
    name = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
