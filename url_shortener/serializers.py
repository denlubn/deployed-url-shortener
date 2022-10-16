from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from url_shortener.models import URL


class URLSerializer(serializers.ModelSerializer):
    original_link = serializers.URLField(
        max_length=1000,
        label="",
        style={'placeholder': 'Shorten your link'}
    )

    class Meta:
        model = URL
        fields = ["id", "original_link", "short_url", "num_visits"]
        read_only_fields = ["id", "short_url", "num_visits"]


class URLDetailSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=URL.objects.all())
        ]
    )

    class Meta:
        model = URL
        fields = ["id", "original_link", "short_url", "num_visits"]
        read_only_fields = ["num_visits"]
