from django.db import models


class InAdmin(models.Model):
    name = models.TextField()


class NotInAdmin(models.Model):
    name = models.TextField()


class Tag(models.Model):
    name = models.TextField()


class Address(models.Model):
    city = models.TextField()


class Producer(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.TextField()


class Product(models.Model):
    name = models.TextField()
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    size = models.IntegerField()
    size_unit = models.TextField()
    default_sku = models.ForeignKey("SKU", null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    onsale = models.BooleanField(null=True)

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
