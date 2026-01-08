from rest_framework import serializers
from .models import Document
from .utils import generate_embedding

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ("embedding",)

    def create(self, validated_data):
        validated_data["embedding"] = generate_embedding(
            validated_data["content"]
        )
        return super().create(validated_data)
