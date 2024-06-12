from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        print("validated_data",validated_data)
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Check if username and email are unique
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')

        user = User.objects.create_user(username=username, email=email, password=password)
        return user