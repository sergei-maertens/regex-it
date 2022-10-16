from django.db import models


class AccessToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    token = models.TextField()
