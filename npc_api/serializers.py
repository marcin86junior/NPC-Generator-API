from rest_framework import serializers
from .models import Story, Character


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title', 'content', 'uploaded_at']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'story', 'name', 'faction', 'profession',
                  'personality_traits', 'background', 'created_at']


class StoryQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)


class CharacterRequestSerializer(serializers.Serializer):
    request = serializers.CharField(max_length=500)
