from rest_framework import serializers

from shortener.models import ShortUrl
from shortener.utils import shortit


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = '__all__'
        extra_kwargs = {
            'pk': {'read_only': True},
            'url_hash': {'read_only': True},
            'redirect_count': {'read_only': True},
            'created_at': {'read_only': True},
            'creator': {'read_only': True},
        }

    def create(self, validated_data: dict) -> ShortUrl:
        full_url: str = validated_data["full_url"]
        validated_data["url_hash"]: str = shortit(full_url)
        validated_data["creator"] = self.context['request'].user
        short_url = ShortUrl(**validated_data)
        short_url.save()
        return short_url

    def update(self, instance: ShortUrl, validated_data: dict) -> ShortUrl:
        full_url: str = validated_data["full_url"]
        validated_data["url_hash"]: str = shortit(full_url)
        return super().update(instance, validated_data)
