from __future__ import unicode_literals

from django.db import models

class HelloWorld(models.Model):
    say = models.CharField(max_length=100)

    def __unicode__(self):
        return self.say
