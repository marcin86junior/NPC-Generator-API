from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stories', views.StoryViewSet)
router.register(r'characters', views.CharacterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stories/<int:story_id>/generate-character/', views.GenerateCharacterView.as_view(), name='generate-character'),
    path('stories/<int:story_id>/generate-name/', views.GenerateCharacterNameView.as_view(), name='generate-name'),
    path('stories/<int:story_id>/ask-question/', views.StoryAskQuestionView.as_view(), name='ask-question'),

    # My additional endpoints:
    path('characters/<int:character_id>/talk/', views.CharacterTalkView.as_view(), name='character-talk'),
]
