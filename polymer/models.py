import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __unicode__(self):
        return u'%s %s' % (self.name, self.email)

class Stash(models.Model):
    owner = models.ForeignKey(User, related_name='owner')
    users = models.ManyToManyField(User) 

    name = models.CharField(max_length=50)
    time = models.DateTimeField('date created', null=True)

    def __unicode__(self):
        return u'%s -  %s' % (self.owner.name, self.name)

class Content(models.Model):
    user = models.ForeignKey(User)
    stash = models.ForeignKey(Stash)

    link = models.CharField(max_length=200)
    time = models.DateTimeField('date added')
    updateTime = models.DateTimeField('date updated')
    
    def __unicode__(self):
        return u'%s by: %s' % (self.link, self.user.name)

class Status(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(Content)

    NEW_STATUS = 1
    VIEWED_STATUS = 2
    UPDATED_STATUS = 3
    ARCHIVED_STATUS = 4
    CHOICES = (
        (NEW_STATUS, 'New'),
        (VIEWED_STATUS, 'Viewed'),
        (UPDATED_STATUS, 'Updated'),
        (ARCHIVED_STATUS, 'Archived'),
    )
    status = models.IntegerField(choices=CHOICES, default=NEW_STATUS)

    def __unicode__(self):
        return u'%s -  %s' % (self.user.name, self.status)

class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(Content)

    text = models.TextField()
    time = models.DateTimeField('date commented')
    # do i need stash and content too?

    def was_commented_recently(self):
        return self.time >= timezone.now() - datetime.timedelta(days=1)

    def __unicode__(self):
        return u'%s - %s' % (self.user.name, self.text)
