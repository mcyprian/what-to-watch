import logging
from datetime import datetime

from .models import (Channel,
                     EPGEntity,
                     Broadcasting,
                     Genre,
                     Person,
                     Actor,
                     ParticipatesIn)

from .serializers import ChannelSerializer, EPGEntitySerializer

logger = logging.getLogger(__name__)


def add_channel(program):
    if Channel.objects.filter(uid=program["@id"]).exists():
        return Channel.objects.get(uid=program["@id"])
    else:
        return ChannelSerializer.create_from_xml_dict(data=program)


def add_epg(channel, data, date):
    if EPGEntity.objects.filter(uid=data["@id"]).exists():
        epg = EPGEntity.objects.get(uid=data["@id"])
    else:
        epg = EPGEntitySerializer.create_from_xml_dict(data=data)

    start_datetime = "/".join([date, data.get("cas-od2")])
    try:
        starts_at = datetime.strptime(start_datetime, "%Y-%m-%d/%H:%M")
    except ValueError:
        logger.error("Entity {0}: invalid format of start date {1}".format(
            data["@id"], start_datetime))
        starts_at = None
    if not Broadcasting.objects.filter(
        channel=channel,
        epg=epg,
        date=starts_at.date(),
        starts_at=starts_at.time()
    ).exists():
        broadcast = Broadcasting(
            channel=channel,
            epg=epg,
            date=starts_at.date(),
            starts_at=starts_at.time(),
        )
        broadcast.save()
    return epg


def add_genres(epg, genre_list):
    if not isinstance(genre_list, list):
        genre_list = [genre_list]
    for genre in genre_list:
        if Genre.objects.filter(title=genre).exists():
            new_genre = Genre.objects.get(title=genre)
        else:
            new_genre = Genre.objects.create(title=genre)
            new_genre.save()
        epg.genres.add(new_genre)


def add_participation(person, epg, role):
    if not ParticipatesIn.objects.filter(
            person=person,
            epg=epg,
            role=role).exists():
        participation = ParticipatesIn(
            person=person,
            epg=epg,
            role=role,
        )
        participation.save()
        return participation


def add_persons(person_list, epg, role):
    if not isinstance(person_list, list):
        person_list = [person_list]
    for person in person_list:
        if Person.objects.filter(name=person["jmeno"]).exists():
            new_person = Person.objects.get(name=person["jmeno"])
        else:
            new_person = Person.objects.create(
                name=person["jmeno"],
            )
            new_person.save()
        add_participation(new_person, epg, role)


def add_actors(actor_list, epg):
    if not isinstance(actor_list, list):
        actor_list = [actor_list]
    for actor in actor_list:
        if Actor.objects.filter(uid=actor["@id"]).exists():
            new_person = Actor.objects.get(uid=actor["@id"])
        else:
            new_person = Actor.objects.create(
                uid=actor["@id"],
                name=actor["jmeno"]
            )
            new_person.save()
        add_participation(new_person, epg, role="actor")
