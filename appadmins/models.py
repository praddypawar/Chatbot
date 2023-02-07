from django.db import models
from appbase.models import Base
# Create your models here.
class Tags(Base):
    tag_name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.tag_name