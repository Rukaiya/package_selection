from django.db import models

# Create your models here.
class Packages(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    details = models.TextField(blank=True, null=True)
    service_ids = models.CharField(max_length=250, blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'packages'

    def __str__(self) -> str:
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    details = models.TextField(blank=True, null=True)
    view_order = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'

    def __str__(self) -> str:
        return self.name