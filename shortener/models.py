from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class ShortUrl(models.Model):
    class Meta:
        db_table = 'short_url'
        ordering = ('created_at',)

    full_url = models.URLField(unique=True)
    url_hash = models.TextField(unique=True)
    redirect_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.pk}: {self.url_hash} - {self.full_url}'
