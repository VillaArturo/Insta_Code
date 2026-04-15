from rest_framework import serializers

class TranslationSerializer(serializers.Serializer):
    source_code = serializers.CharField()
    language = serializers.CharField(default='vb6')