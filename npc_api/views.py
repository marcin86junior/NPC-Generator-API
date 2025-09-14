from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Story, Character
from .serializers import (
    StorySerializer,
    CharacterSerializer,
    StoryQuestionSerializer,
    CharacterRequestSerializer,
    CharacterTalkSerializer
)
from .services.story_understanding import StoryUnderstanding
from .services.character_generator import CharacterGenerator
from .services.character_conversation import CharacterConversation

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class StoryAskQuestionView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['question'],
            properties={
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='Pytanie do historii')
            }
        ),
        responses={200: openapi.Response('Odpowiedź na pytanie', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answer': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))}
    )
    def post(self, request, story_id):
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return Response({"error": "Historia nie istnieje"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoryQuestionSerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.validated_data['question']
            story_understanding = StoryUnderstanding(story_content=story.content)
            answer = story_understanding.answer_question(question)

            return Response({'answer': answer})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class GenerateCharacterView(views.APIView):
    @swagger_auto_schema(
        request_body=CharacterRequestSerializer,
        responses={
            201: openapi.Response('Generated name', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Generated character name')
                }
            ))
        }
    )
    def post(self, request, story_id):
        try:
            story = Story.objects.get(pk=story_id)
        except Story.DoesNotExist:
            return Response(
                {"error": "Story with the given ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CharacterRequestSerializer(data=request.data)

        if serializer.is_valid():
            story_understanding = StoryUnderstanding(story_content=story.content)
            character_generator = CharacterGenerator(story_understanding)

            character_request = serializer.validated_data['request']
            character_data = character_generator.generate_character_details(request=character_request)

            character = Character(
                story=story,
                name=character_data['name'],
                faction=character_data['faction'],
                profession=character_data['profession'],
                personality_traits=character_data['personality_traits'],
                background=character_data['background']
            )
            character.save()

            return Response(CharacterSerializer(character).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateCharacterNameView(views.APIView):
    @swagger_auto_schema(
        request_body=CharacterRequestSerializer,
        responses={
            201: openapi.Response('Generated name', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Generated character name')
                }
            ))
        }
    )
    def post(self, request, story_id):
        try:
            story = Story.objects.get(pk=story_id)
        except Story.DoesNotExist:
            return Response(
                {"error": "Story with the given ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CharacterRequestSerializer(data=request.data)

        if serializer.is_valid():
            story_understanding = StoryUnderstanding(story_content=story.content)
            character_generator = CharacterGenerator(story_understanding)

            character_request = serializer.validated_data['request']
            name = character_generator.generate_character_name(character_request)

            return Response({'name': name})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterTalkView(APIView):
    @swagger_auto_schema(
        operation_description="Wysyła wiadomość do postaci i generuje odpowiedź zgodnie z jej osobowością",
        request_body=CharacterTalkSerializer,
        responses={
            200: openapi.Response('Odpowiedź postaci', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'response': openapi.Schema(type=openapi.TYPE_STRING, description='Odpowiedź postaci')
                }
            )),
            400: 'Nieprawidłowe dane wejściowe',
            404: 'Postać nie znaleziona',
            500: 'Błąd generowania odpowiedzi'
        }
    )
    def post(self, request, character_id):
        try:
            # Pobierz postać na podstawie ID
            character = Character.objects.get(pk=character_id)
        except Character.DoesNotExist:
            return Response(
                {"error": "Postać o podanym ID nie istnieje"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CharacterTalkSerializer(data=request.data)

        if serializer.is_valid():
            # Pobierz wiadomość od użytkownika
            message = serializer.validated_data['message']

            try:
                # Inicjalizuj serwis konwersacji
                conversation_service = CharacterConversation(character=character)

                # Wygeneruj odpowiedź
                response = conversation_service.generate_response(message)

                return Response({'response': response})
            except Exception as e:
                return Response(
                    {"error": f"Wystąpił błąd: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
