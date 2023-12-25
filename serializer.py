from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import EEG_DataM,DemoM

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def validateEmailToken(request):
        data = json.loads(request.body.decode('utf-8'))
        token = data['token']
        res = {
            'status': 'success',
            'message': 'Valid',
        }
    
        if GeneralUser.objects.filter(email_verified_hash=token, email_verified=0).exists():
            tokenExists = GeneralUser.objects.get(email_verified_hash=token, email_verified=0)

            tokenExists.email_verified = 1
            tokenExists.save()

        else:
            res = {
                'status': 'failed',
                'message': 'Invalid',
                }
    
        return JsonResponse(res) 
    
class EEGDSerializer(serializers.ModelSerializer):
    class Meta:
        model=EEG_DataM
        fields=('EFileId', 'EFileName')
class DEMOSerializer(serializers.ModelSerializer):
    class Meta:
        model=DemoM
        fields=('DFileId', 'DFileName')