import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Stash(models.Model):
    owner = models.ForeignKey(User, related_name='owner')
    users = models.ManyToManyField(User) 

    name = models.CharField(max_length=50)
    time = models.DateTimeField('date created', null=True)

    def __unicode__(self):
        return u'%s -  %s' % (self.owner.name, self.name)
    
    def to_json(self):
        return {
                'id' : self.id,
                'name' : self.name,
                'time' : self.time.ctime(),
                'owner' : {'name': self.owner.get_username(), 'id': self.owner.id},
                'users' : [{'name':u.get_username(), 'id':u.id} for u in self.users.all()] 
                }

class Content(models.Model):
    user = models.ForeignKey(User)
    stash = models.ForeignKey(Stash)

    link = models.CharField(max_length=200)
    time = models.DateTimeField('date added')
    updateTime = models.DateTimeField('date updated')
    
    def __unicode__(self):
        return u'%s by: %s' % (self.link, self.user.get_username())

    def to_json(self, user):
        return {
                'id' : self.id,
                'user' : self.user.get_username(),
                'time' : self.time.ctime(),
                'updateTime' : self.updateTime.ctime(),
                'link' : self.link,
                'status' : Status.objects.filter(content = self).get(user=user).to_json(),
                'comments' : [c.to_json() for c in Comment.objects.filter(content = self)]
                }

class Status(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(Content)

    NEW_STATUS = 0
    VIEWED_STATUS = 1
    UPDATED_STATUS = 2
    ARCHIVED_STATUS = 3
    CHOICES = (
        (NEW_STATUS, 'New'),
        (VIEWED_STATUS, 'Viewed'),
        (UPDATED_STATUS, 'Updated'),
        (ARCHIVED_STATUS, 'Archived'),
    )
    status = models.IntegerField(choices=CHOICES, default=NEW_STATUS)

    def __unicode__(self):
        return u'%s -  %s' % (self.user.get_username(), self.status)

    def to_json(self):
        return self.CHOICES[self.status][1]

class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(Content)

    text = models.TextField()
    time = models.DateTimeField('date commented')

    def was_commented_recently(self):
        return self.time >= timezone.now() - datetime.timedelta(days=1)

    def __unicode__(self):
        return u'%s - %s' % (self.user.get_username(), self.text)

    def to_json(self):
        return {
                'id' : self.id,
                'user' : {'name':self.user.get_username(), 'id':self.user.id},
                'time' : self.time.ctime(),
                'text' : self.text
                }
