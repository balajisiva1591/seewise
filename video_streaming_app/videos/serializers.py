from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Video
        fields = ['id', 'user', 'name', 'video_url']
