from rest_framework import serializers

class RAGQuerySerializer(serializers.Serializer):
    question = serializers.CharField()
    top_k = serializers.IntegerField(default=3, required=False)
