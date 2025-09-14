from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Character(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=255)
    faction = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    personality_traits = models.JSONField()
    background = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ConversationHistory(models.Model):
    CHARACTER = "CHARACTER"
    USER = "USER"
    SENDER_CHOICES = [
        (CHARACTER, 'Character'),
        (USER, 'User'),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField(verbose_name="Message content")
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Message author")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "Character" if self.sender_type == self.CHARACTER else "User"
        return f"{sender} ({self.character.name}): {self.message[:50]}..."

    class Meta:
        verbose_name = "Conversation message"
        verbose_name_plural = "Conversation history"
        ordering = ['timestamp']
