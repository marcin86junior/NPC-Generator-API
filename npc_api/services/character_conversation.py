import os
import google.generativeai as genai


class CharacterConversation:
    def __init__(self, character=None, api_key=None):
        """
        Initialization of the character conversation service.

        Args:
            character: Character object from the Character model
            api_key: Optional Gemini API key
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

        self.character = character
        self.model = "gemini-2.0-flash-lite"

        # Prepare character description
        if character:
            self.character_description = self._prepare_character_description()

    def _prepare_character_description(self):
        """
        Prepares a character description based on its attributes.
        """
        personality = (
            self.character.personality_traits
            if isinstance(self.character.personality_traits, str)
            else str(self.character.personality_traits)
        )

        return {
            "name": self.character.name,
            "faction": self.character.faction,
            "profession": self.character.profession,
            "personality": personality,
            "background": self.character.background
        }

    def _is_good_personality(self):
        """
        Checks if the character has a good personality.

        Returns:
        bool: True if the character has a good personality, False otherwise
        """
        good_traits = ['good', 'kind', 'helpful', 'honest', 'fair', 'noble']
        bad_traits = ['evil', 'bad', 'cruel', 'selfish', 'cunning', 'ruthless']

        personality = str(self.character.personality_traits).lower()

        good_count = sum(1 for trait in good_traits if trait in personality)
        bad_count = sum(1 for trait in bad_traits if trait in personality)

        return good_count >= bad_count

    def generate_response(self, message):
        """
        Generates a character's response to the user's message.

        Args:
            message: Message from the user

        Returns:
            str: Generated character response
        """
        try:
            is_good = self._is_good_personality()
            personality_type = "good, helpful, and friendly" if is_good else "malicious, selfish, and suspicious"

            prompt = f"""
            Assume the role of a character with the following traits:
            - Name: {self.character.name}
            - Faction: {self.character.faction}
            - Profession: {self.character.profession}
            - Personality: {self.character.personality_traits}
            - Background: {self.character.background}

            Your character has a {personality_type} personality.

            The user wrote to you: "{message}"

            Respond as this character, maintaining their unique character and manner of speaking.
            The response should be short (2-3 sentences) and fully reflect the character's personality.
            """

            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)

            return response.text
        except Exception as e:
            return f"Error while generating response: {str(e)}"
