from django.db import models

class Bookmark(models.Model):
    title = models.CharField('TiTLE', max_length=100)
    url = models.URLField('URL', unique=True)

    def __str__(self):
        return self.title