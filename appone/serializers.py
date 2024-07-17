from rest_framework import serializers
from appone.models  import User,FoodItem,AddtoBag,Address,PlaceOrder

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields="__all__"

    def validate(self, attrs):
        if attrs['password'] != attrs["password2"]:
            raise serializers.ValidationError({"msg":"password did not match"})
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializers(serializers.Serializer):
    email=serializers.CharField()
    password=serializers.CharField(write_only=True)


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodItem
        fields="__all__"


class AddtoBagSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddtoBag
        fields="__all__"

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"

class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PlaceOrder
        fields="__all__"