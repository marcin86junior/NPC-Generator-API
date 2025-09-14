# My first Gemini chat bot
# www.youtube.com/watch?v=qfWpPEgea2A

from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.0-flash-lite")

while True:
    message = input("You: ")
    if message == "exit":
        break

    res = chat.send_message(message)
    print("Bot:", res.text)
