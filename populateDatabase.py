import django
from django.utils import timezone
from models import *

django.setup()

maxwell = User(name='maxwell', email='maxwell.mosley@gmail.com')
maxwell.save()
ishita = User(name='ishita', email='ishitaaloni@gmail.com')
ishita.save()
morgan = User(name='morgan', email='morgan.neiman@gmail.com')
morgan.save()
kenny = User(name='kenny', email='kennydeakins@gmail.com')
kenny.save()
bunker = User(name='bunker', email='bunkaroo@gmail.com')
bunker.save()

#maxwell stash
maxwellStash = Stash(name="maxwell's stash", time=timezone.now() - datetime.timedelta(hours=2), owner=maxwell)
maxwellStash.save()
maxwellStash.users.add(maxwell)

imgurContent = Content(user=maxwell, stash=maxwellStash, link='www.imgur.com', time=timezone.now(), updateTime=timezone.now())
imgurContent.save()

googleContent = Content(user=maxwell, stash=maxwellStash, link='www.google.com', time=timezone.now() - datetime.timedelta(hours=1), updateTime=timezone.now() - datetime.timedelta(hours=1))
googleContent.save()

Status(user=maxwell, content=imgurContent).save()
Status(user=maxwell, content=googleContent).save()

#ishita stash is empty
ishitaStash = Stash(name="ishita's stash", time=timezone.now() - datetime.timedelta(hours=2), owner=ishita)
ishitaStash.save()
ishitaStash.users.add(ishita)

#poopy stash
poopyStash = Stash(name='poopy stash', time=timezone.now(), owner=maxwell)
poopyStash.save()
poopyStash.users.add(maxwell, ishita)

imgurContent = Content(user=maxwell, stash=poopyStash, link='www.imgur.com', time=timezone.now(), updateTime=timezone.now())
imgurContent.save()

googleContent = Content(user=ishita, stash=poopyStash, link='www.google.com', time=timezone.now() - datetime.timedelta(hours=1), updateTime=timezone.now() - datetime.timedelta(hours=1))
googleContent.save()

Status(user=maxwell, content=imgurContent, status=3).save()
Status(user=maxwell, content=googleContent, status=3).save()
Status(user=ishita, content=imgurContent, status=4).save()
Status(user=ishita, content=googleContent, status=2).save()

Comment(user=ishita, content=imgurContent, text='why did you share this?', time=timezone.now()).save()
Comment(user=ishita, content=googleContent, text='why did you share this one too?', time=timezone.now()).save()
