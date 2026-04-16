from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name","last_name", "username","password"
        ]
        write_only_fields = [
            "password"
        ]
