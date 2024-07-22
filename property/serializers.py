from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email_address', 'phone_number', 'password', 'user_type']

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email_address=validated_data['email_address'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
