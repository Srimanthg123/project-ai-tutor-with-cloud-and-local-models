from google import genai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini (NEW SDK)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_cloud_explanation(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"[Cloud Error] {e}"

def get_local_explanation(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": f"Explain this concept creatively for a beginner:\n{prompt}",
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"[Local Error] {e}"

def main():
    print("=== Study Buddy – AI Tutor ===")
    while True:
        user_input = input("\nEnter an AI concept (or 'quit'): ")
        if user_input.lower() == "quit":
            print("Goodbye! Keep learning with AI 🚀")
            break

        print("\n[1] Cloud Model (Gemini) – Factual Explanation")
        print(get_cloud_explanation(user_input))

        print("\n[2] Local Model (Ollama – Llama 3.1) – Creative Explanation")
        print(get_local_explanation(user_input))

if __name__ == "__main__":
    main()