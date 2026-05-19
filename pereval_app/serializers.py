from .models import *
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']

class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        try:
            user = User.objects.get(email=user_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create(**user_data)

        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        pereval = Pereval.objects.create(
            **validated_data,
            user=user,
            coords=coords,
            level=level,
            status='new',
        )

        for image in images_data:
            Images.objects.create(pereval=pereval, **image)

        return pereval