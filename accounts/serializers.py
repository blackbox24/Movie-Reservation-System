from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            "first_name","last_name", "username","password"
        ]
    def save(self, **kwargs):
        print(kwargs)
        password = kwargs.pop("password")
        user = super().save(**kwargs)
        user.set_password(password)
        user.save()
        return user
