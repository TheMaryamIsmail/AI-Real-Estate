import os
import google.generativeai as genai

class RealEstateChatbot:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "your-api-key-here")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3.8-flash')
        
    def ask(self, prompt: str) -> str:
        system_instruction = (
            "You are an expert AI Real Estate Assistant. Your role is to help users understand property markets, "
            "provide buying guidance, summarize real estate listings, and answer housing questions professionally and concisely."
        )
        full_prompt = f"{system_instruction}\n\nUser Question: {prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text
