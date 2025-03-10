from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class DocumentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created', 'updated', 'tags', 'tag_ids']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        document = Document.objects.create(**validated_data)
        document.tags.set(Tag.objects.filter(id__in=tag_ids))
        return document

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            instance.tags.set(Tag.objects.filter(id__in=tag_ids))

        return instance

