from rest_framework import serializers

#Filtro de datos de Cliente-Backend
class TranslationSerializer(serializers.serializer):
    source_code = serializers.CharField()
    language = serializers.CharField(default='vb6')