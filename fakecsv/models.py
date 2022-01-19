import datetime

from django.conf import settings
from django.db import models


class Schema(models.Model):
    """ I decided to create Schema with read instructions in csv format separated with semicolons
     each row type is like: column_id,object_type,object_id.
     Objects will usually be called similar, so it will achieve more rational memory usage """

    name = models.CharField(max_length=25)
    separator = models.CharField(max_length=2)
    string = models.CharField(max_length=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_instructions = models.CharField(max_length=1000)
    modified_date = models.DateField(default=datetime.date.today)
    created_date = models.DateField(null=True)
    file = models.FileField()

    def __str__(self):
        return self.name


class SchemaBase(models.Model):
    """ Model sub-class for creating models connected to schema"""

    name = models.CharField(max_length=25)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SchemaBaseRange(SchemaBase):
    """ SchemaBase sub-class for creating models with specified range"""
    min_range = models.IntegerField()
    max_range = models.IntegerField()

    class Meta:
        abstract = True


class FullName(SchemaBase):
    pass


class Job(SchemaBase):
    pass


class Email(SchemaBase):
    pass


class DomainName(SchemaBase):
    pass


class PhoneNumber(SchemaBase):
    pass


class CompanyName(SchemaBase):
    pass


class Text(SchemaBaseRange):
    pass


class Integer(SchemaBaseRange):
    pass


class Address(SchemaBase):
    pass


class Date(SchemaBase):
    pass
