import os
from google import genai
from django.conf import settings


class StoryUnderstanding:
    def __init__(self, story_content=None, story_file_path=None, api_key=None):
        """Initialization with story text or file path."""

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

        if story_content:
            self.story_content = story_content
        elif story_file_path:
            self.story_content = self._load_story(story_file_path)
        else:
            # Load from Django configuration by default
            self.story_content = self._load_story(settings.STORY_FILE_PATH)

        self.model = "gemini-2.0-flash-lite"
        self.story_summary = self._generate_summary()

    def _load_story(self, file_path):
        """Load story content from file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _generate_summary(self):
        """Generate a summary of the story for internal use."""

        try:
            prompt = (f"Analyze this story and create a detailed summary with key elements such as world,"
                      f" factions, cultures, history, and other important details that will help in character generation:"
                      f"\n\n{self.story_content}")

            chat = self.client.chats.create(model=self.model)
            response = chat.send_message(prompt)

            return response.text
        except Exception as e:
            return f"Error during summary generation: {str(e)}"

    def answer_question(self, question):
        """Answer questions about the story."""

        try:
            prompt = f"Story:\n\n{self.story_content}\n\nQuestion: {question}"

            chat = self.client.chats.create(model=self.model)
            response = chat.send_message(prompt)

            return response.text
        except Exception as e:
            return f"Error while answering the question: {str(e)}"
