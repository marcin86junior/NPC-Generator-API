from rest_framework import serializers
from .models import Story, Character, ConversationHistory


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
    question = serializers.CharField(max_length=300)


class CharacterRequestSerializer(serializers.Serializer):
    request = serializers.CharField(max_length=300)


class CharacterTalkSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        help_text="Message to the character"
    )


class ConversationHistorySerializer(serializers.ModelSerializer):
    character_name = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = ConversationHistory
        fields = ['id', 'character', 'character_name', 'message', 'sender_type', 'sender', 'timestamp']
        read_only_fields = ['timestamp']

    def get_character_name(self, obj):
        return obj.character.name if obj.character else None

    def get_sender(self, obj):
        return "Character" if obj.sender_type == ConversationHistory.CHARACTER else "User"
