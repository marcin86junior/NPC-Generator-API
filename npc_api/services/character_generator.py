import os
import json
from google import genai


class CharacterGenerator:
    def __init__(self, story_understanding, api_key=None):
        """Initialization with StoryUnderstanding object."""

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.story_understanding = story_understanding
        self.model = "gemini-2.0-flash-lite"
        self.generated_names = set()

    def generate_character_name(self, request):
        """Generate a character name based on the user's request."""

        prompt = f"""
        Based on the story world below and the user's request, generate a unique name that fits the world for a character.

        World summary:
        {self.story_understanding.story_summary}

        User request: {request}

        Previously generated names (avoid them): {', '.join(self.generated_names)}

        Return only the character name, nothing else.
        """

        chat = self.client.chats.create(model=self.model)
        response = chat.send_message(prompt)

        name = response.text.strip()
        self.generated_names.add(name)
        return name

    def generate_character_details(self, name=None, request=None):
        """Generate complete character details in JSON format."""

        if name is None and request is not None:
            name = self.generate_character_name(request)

        prompt = f"""
        Create detailed attributes for the character "{name}" that are consistent with the story world.

        World summary:
        {self.story_understanding.story_summary}

        User request (if any): {request or "No specific request"}

        Generate a JSON object with the following fields:
        - name: Character's name
        - faction: Which faction of the world they belong to
        - profession: Their occupation or role
        - personality_traits: Array of 2-4 personality traits
        - background: Brief history (1-2 sentences)

        Return only valid JSON, nothing else.
        """

        chat = self.client.chats.create(model=self.model)
        response = chat.send_message(prompt)

        character_json = response.text

        # Cleaning the response to ensure a valid JSON format
        character_json = character_json.strip()
        if character_json.startswith("```json"):
            character_json = character_json[7:]
        if character_json.endswith("```"):
            character_json = character_json[:-3]

        try:
            character_data = json.loads(character_json.strip())
            return character_data
        except json.JSONDecodeError:
            # If the JSON format is invalid, try again
            retry_prompt = f"""
                Create a valid JSON object for the character "{name}". Return only clean JSON:
                {{
                  "name": "character name",
                  "faction": "faction",
                  "profession": "occupation",
                  "personality_traits": ["trait1", "trait2"],
                  "background": "background story"
                }}
                """
            retry_response = self.client.generate_content(
                model=self.model,
                contents=retry_prompt
            )
            character_json = retry_response.text.strip()
            return json.loads(character_json)
