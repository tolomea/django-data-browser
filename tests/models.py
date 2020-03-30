from django.db import models


class Producer(models.Model):
    name = models.TextField()


class Product(models.Model):
    name = models.TextField()
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    size = models.IntegerField()
    size_unit = models.TextField()

    def is_onsale(self):
        return False
