from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Story, Character, ConversationHistory
from .serializers import (
    StorySerializer,
    CharacterSerializer,
    StoryQuestionSerializer,
    CharacterRequestSerializer,
    CharacterTalkSerializer,
    ConversationHistorySerializer,

)
from .services.story_understanding import StoryUnderstanding
from .services.character_generator import CharacterGenerator
from .services.character_conversation import CharacterConversation

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render


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
        operation_description="Sends a message to the character and generates a response according to their personality",
        request_body=CharacterTalkSerializer,
        responses={
            200: openapi.Response('Character response', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'response': openapi.Schema(type=openapi.TYPE_STRING, description='Character response')
                }
            )),
            400: 'Invalid input data',
            404: 'Character not found',
            500: 'Response generation error'
        }
    )
    def post(self, request, character_id):
        try:
            # Retrieve character by ID
            character = Character.objects.get(pk=character_id)
        except Character.DoesNotExist:
            return Response(
                {"error": "Character with the given ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CharacterTalkSerializer(data=request.data)

        if serializer.is_valid():
            # Get message from user
            message = serializer.validated_data['message']

            try:
                # Initialize the conversation service
                conversation_service = CharacterConversation(character=character)

                # Generate response
                response = conversation_service.generate_response(message)

                return Response({'response': response})
            except Exception as e:
                return Response(
                    {"error": f"An error occurred: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationHistoryViewSet(viewsets.ModelViewSet):
    queryset = ConversationHistory.objects.all().order_by('-timestamp')
    serializer_class = ConversationHistorySerializer
    filterset_fields = ['character', 'sender_type']
    search_fields = ['message']

    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character_id')
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        return queryset


class ConversationHistoryTemplateView(TemplateView):
    template_name = "npc_api/conversation_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character_id = self.kwargs.get('character_id')

        character = get_object_or_404(Character, pk=character_id)
        conversations = ConversationHistory.objects.filter(character=character).order_by('timestamp')

        page = self.request.GET.get('page', 1)
        paginator = Paginator(conversations, 20)
        paginated_conversations = paginator.get_page(page)

        context['character'] = character
        context['conversations'] = paginated_conversations
        return context

def main_page(request):
    return render(request, 'npc_api/main.html')

def world_page(request):
    stories = Story.objects.all()
    return render(request, 'npc_api/world.html', {'stories': stories})

def characters_page(request):
    characters = Character.objects.all()
    return render(request, 'npc_api/characters.html', {'characters': characters})

def conversation_page(request):
    characters = Character.objects.all()
    return render(request, 'npc_api/conversation.html', {'characters': characters})

def quick_add_fantasy(request):
    try:
        with open('data/fantasy.md', 'r', encoding='utf-8') as file:
            fantasy_content = file.read()
        story = Story.objects.create(
            title="Fantasy World",
            content=fantasy_content
        )
        from django.shortcuts import redirect
        return redirect('world')
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f"Wystąpił błąd podczas dodawania historii: {str(e)}")


def about_page(request):
    return render(request, 'npc_api/about.html')

