import os
import google.generativeai as genai
from django.conf import settings


class CharacterConversation:
    def __init__(self, character=None, api_key=None):
        """
        Inicjalizacja serwisu do konwersacji z postacią.

        Args:
            character: Obiekt postaci z modelu Character
            api_key: Opcjonalny klucz API do Gemini
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

        self.character = character
        self.model = "gemini-2.0-flash-lite"

        # Przygotowanie opisu postaci
        if character:
            self.character_description = self._prepare_character_description()

    def _prepare_character_description(self):
        """
        Przygotowuje opis postaci na podstawie jej atrybutów.
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
        Sprawdza, czy postać ma dobrą osobowość.

        Returns:
            bool: True jeśli postać ma dobrą osobowość, False w przeciwnym przypadku
        """
        good_traits = ['good', 'kind', 'helpful', 'honest', 'fair', 'noble']
        bad_traits = ['evil', 'bad', 'cruel', 'selfish', 'cunning', 'ruthless']

        personality = str(self.character.personality_traits).lower()

        good_count = sum(1 for trait in good_traits if trait in personality)
        bad_count = sum(1 for trait in bad_traits if trait in personality)

        return good_count >= bad_count

    def generate_response(self, message):
        """
        Generuje odpowiedź postaci na wiadomość użytkownika.

        Args:
            message: Wiadomość od użytkownika

        Returns:
            str: Wygenerowana odpowiedź postaci
        """
        try:
            is_good = self._is_good_personality()
            personality_type = "dobra, pomocna i przyjazna" if is_good else "złośliwa, samolubna i podejrzliwa"

            prompt = f"""
            Wciel się w postać o poniższych cechach:
            - Imię: {self.character.name}
            - Frakcja: {self.character.faction}
            - Profesja: {self.character.profession}
            - Osobowość: {self.character.personality_traits}
            - Historia: {self.character.background}

            Twoja postać ma {personality_type} osobowość.

            Użytkownik napisał do ciebie: "{message}"

            Odpowiedz jako ta postać, zachowując jej unikalny charakter i sposób wypowiedzi.
            Odpowiedź powinna być krótka (2-3 zdania) i w pełni odzwierciedlać osobowość postaci.
            """

            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)

            return response.text
        except Exception as e:
            return f"Błąd podczas generowania odpowiedzi: {str(e)}"
