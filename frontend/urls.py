from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', include(router.urls)),
    path('stories/<int:story_id>/ask-question/', views.StoryAskQuestionView.as_view(), name='ask-question'),
    path('characters/<int:story_id>/generate-name/', views.GenerateCharacterNameView.as_view(), name='generate-name'),
    path('characters/<int:story_id>/generate-character/', views.GenerateCharacterView.as_view(), name='generate-character'),
    path('conversations/<int:character_id>/talk/', views.CharacterTalkView.as_view(), name='character-talk'),
]
