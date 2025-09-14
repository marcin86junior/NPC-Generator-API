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
    SENDER_CHOICES = [(CHARACTER, 'Character'), (USER, 'User'),]

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField(verbose_name="Treść wiadomości")
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Autor wiadomości")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "Postać" if self.sender_type == self.CHARACTER else "Użytkownik"
        return f"{sender} ({self.character.name}): {self.message[:50]}..."

    class Meta:
        verbose_name = "Wiadomość konwersacji"
        verbose_name_plural = "Historia konwersacji"
        ordering = ['timestamp']
