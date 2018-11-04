import logging
from datetime import datetime

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import Channel, Genre, EPGEntity, Person, Actor
from .serializers import (ChannelSerializer,
                          EPGEntitySerializer,
                          GenreSerializer,
                          PersonSerializer)
from .utils import unpack_archive
from .helpers import add_channel, add_epg, add_genres, add_persons, add_actors

logger = logging.getLogger(__name__)


@api_view(['POST'])
def update_data(request):
    url = request.data.get('url', None)
    if not url:
        logger.error("URL not specified.")
        return HttpResponse("URL not specified.")
    raw_data = unpack_archive(url)
    if not raw_data:
        logger.error("Failed to fetch data from {0}".format(
            url))
        return HttpResponse("Failed to fetch data from {0}".format(
            url))
    for item in raw_data:
        program = item.get("program")
        if program:
            channel = add_channel(program)
            show_data = program.get("porad")
            if show_data:
                for show in show_data.get("porad", []):
                    epg = add_epg(channel, show, show_data.get("@datum"))

                    actors = show.get("hraji", {}).get("osoba", [])
                    add_actors(actors, epg)

                    directors = show.get("rezie", {}).get("osoba", [])
                    add_persons(directors, epg, role="director")

                    producers = show.get("produkce", {}).get("osoba", [])
                    add_persons(producers, epg, role="producer")

                    genres = show.get("genres", {}).get("genre", [])
                    add_genres(epg, genres)
    logger.info("Data updated successfuly from url {0}".format(url))
    return HttpResponse("Data updated!")


class EPGEntityList(generics.ListCreateAPIView):
    queryset = EPGEntity.objects.all()
    serializer_class = EPGEntitySerializer

    def get_queryset(self):
        queryset = EPGEntity.objects.all()
        genre_title = self.request.query_params.get('genre', None)
        actor_name = self.request.query_params.get('actor', None)
        date = self.request.query_params.get('date', None)
        starts_at = self.request.query_params.get('time', None)
        try:
            if genre_title is not None:
                genre = Genre.objects.get(title=genre_title)
                queryset = queryset.filter(genres__id__exact=genre.id)
            if actor_name is not None:
                actor = Actor.objects.get(name=actor_name)
                queryset = queryset.filter(persones__id__exact=actor.id)
            if date is not None:
                date = datetime.strptime(date, "%Y-%m-%d")
                queryset = queryset.filter(broadcasting__date=date.date())
            if starts_at is not None:
                starts_at = datetime.strptime(starts_at, "%H:%M")
                queryset = queryset.filter(
                    broadcasting__starts_at=starts_at.time())

        except ObjectDoesNotExist:
            logger.warning("Filtered genre or actor doesn't exists")
            return EPGEntity.objects.none()
        except ValueError:
            logger.warning("Specified format of date or time is invalid")
            return EPGEntity.objects.none()
        return queryset


class EPGEntityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EPGEntity.objects.all()
    serializer_class = EPGEntitySerializer


class ChannelList(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
