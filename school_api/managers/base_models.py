from django.db import models
class BaseModels(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True