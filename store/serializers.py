from rest_framework import serializers

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'