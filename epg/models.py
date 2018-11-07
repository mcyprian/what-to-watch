from django.db import models
from django.conf import settings
from stdimage.models import StdImageField


class Channel(models.Model):
    uid = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=128)
    order = models.PositiveIntegerField(null=True)
    channel_type = models.CharField(max_length=128, null=True)
    television = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class EPGEntity(models.Model):
    uid = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=128)
    length = models.PositiveIntegerField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)
    original_title = models.CharField(max_length=128, null=True)
    year = models.PositiveIntegerField(null=True)
    state = models.CharField(max_length=128, null=True)
    rating = models.CharField(max_length=128, null=True)
    genres = models.ManyToManyField(Genre)
    persones = models.ManyToManyField("Person", through="ParticipatesIn")
    channels = models.ManyToManyField(Channel, through="Broadcasting")

    @property
    def actors(self):
        return self.persones.filter(participatesin__role="actor")

    def __str__(self):
        return self.title


class Broadcasting(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    epg = models.ForeignKey(EPGEntity, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    starts_at = models.TimeField(null=True)

    def __str__(self):
        return "{0}: {1} at {2}".format(self.channel, self.epg, self.starts_at)


class Person(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Actor(Person):
    uid = models.BigIntegerField(null=True, unique=True)


class ParticipatesIn(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    epg = models.ForeignKey(EPGEntity, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
    role_name = models.CharField(max_length=128, null=True)

    def __str__(self):
        return "{0}: {1} ({2})".format(self.epg, self.role, self.actor)


class Image(models.Model):
    url = models.CharField(max_length=128, unique=True)
    photo = StdImageField(upload_to=settings.MEDIA_URL,
                          blank=True,
                          variations={
                              'large': (400, 225, True),
                              'medium': (270, 225, True),
                          })
    epg = models.ForeignKey(EPGEntity, on_delete=models.CASCADE)
