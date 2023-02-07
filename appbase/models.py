from django.db import models

# Create your models here.
class Base(models.Model):
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True