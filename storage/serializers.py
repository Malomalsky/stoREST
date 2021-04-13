from rest_framework import serializers

from .models import Resource


class ResourceSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=50)
    amount = serializers.FloatField()
    unit = serializers.CharField(max_length=7)
    price = serializers.FloatField()
    date = serializers.DateField()

    class Meta:
        model = Resource

    def create(self, validated_data):
        return Resource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Метод для PUT-запроса
        """
        instance.title = validated_data.get('title', instance.title)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.price = validated_data.get('price', instance.price)
        instance.date = validated_data.get('date', instance.date)

        instance.save()
        return instance
