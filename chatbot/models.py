from django.db import models

from uuid import uuid4

from django.contrib.auth.models import User


class ChatBot(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    uuid = models.UUIDField(default=uuid4)
    website_url = models.URLField()

    @property
    def index_name(self): 
        return self.name + '-' + self.uuid
