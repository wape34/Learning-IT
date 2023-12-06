from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def save(self, **kwargs):
        self.is_valid()
        user = MyUser.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = MyUser.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
        return new_user


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height', ]


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = Images
        fields = ['title', 'data']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalSerializer(WritableNestedModelSerializer):
    user_id = MyUserSerializer()
    coord_id = CoordSerializer()
    level_id = LevelSerializer(allow_null=True, default=False)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user_id', 'coord_id',
                  'level_id', 'images']
