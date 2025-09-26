from rest_framework.serializers import ModelSerializer

from images.models import Gallery, Image


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
