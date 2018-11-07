from rest_framework import serializers

from . models import Channel, EPGEntity, Genre, Person, Actor


class ChannelSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uid = validated_data.get('uid', instance.uid)
        instance.title = validated_data.get('title', instance.title)
        instance.order = validated_data.get('order', instance.order)
        instance.channel = validated_data.get('channel', instance.channel)
        instance.television = validated_data.get(
            'television', instance.television)

    @staticmethod
    def create_from_xml_dict(data):
        channel = Channel.objects.create(
            uid=data["@id"],
            title=data["@stanice"],
            order=data.get("@poradi"),
            channel_type=data.get("@typ-stanice"),
            television=data.get("@televize"),
        )
        channel.save()
        return channel

    class Meta:
        model = Channel
        fields = ('id', 'uid', 'title', 'order', 'channel_type', 'television')


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)

    class Meta:
        model = Genre
        fields = ('id', 'title',)


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

    class Meta:
        model = Person
        fields = ('id', 'name',)


class ActorSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uid = validated_data.get('uid', instance.uid)
        instance.name = validated_data.get('name', instance.name)

    class Meta:
        model = Actor
        fields = ('id', 'uid', 'name')


class EPGEntitySerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return EPGEntity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uid = validated_data.get('uid', instance.uid)
        instance.title = validated_data.get('title', instance.title)
        instance.original_title = validated_data.get(
            'original_title', instance.original_title)
        instance.length = validated_data.get('length', instance.length)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.year = validated_data.get('year', instance.year)
        instance.state = validated_data.get('state', instance.state)
        instance.rating = validated_data.get('rating', instance.rating)

    @staticmethod
    def create_from_xml_dict(data):
        original_title = data.get("nazev-originalni")
        if original_title and isinstance(original_title, list):
            original_title = original_title[0]
        epg = EPGEntity.objects.create(
            uid=data["@id"],
            title=data["nazev"],
            original_title=original_title,
            length=data.get("delka"),
            summary=data.get("kratkypopis"),
            description=data.get("dlouhypopis"),
            year=data.get("rok-vyroby"),
            state=data.get("zeme", {}).get("@code"),
            rating=data.get("rating"),
        )
        epg.save()
        return epg

    def get_actors(self, obj):
        return obj.persones.filter(role='actor')

    class Meta:
        model = EPGEntity
        fields = (
            'id',
            'uid',
            'title',
            'original_title',
            'length',
            'summary',
            'description',
            'year',
            'state',
            'rating',
            'genres',
            'actors')
