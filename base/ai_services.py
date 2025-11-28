import google.generativeai as genai
from django.conf import settings

class GeminiAIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')  # FIXED MODEL NAME
    
    def generate_medical_suggestions(self, symptoms):
        prompt = f"""
        You are a medical AI assistant. A user describes: "{symptoms}"
        
        Provide a structured, helpful response:

        POSSIBLE CONDITIONS:
        - List 2–3 common explanations

        RECOMMENDED ACTIONS:
        - Home care + what to do now

        RED FLAGS:
        - When to seek urgent medical help

        WHEN TO SEE A DOCTOR:
        - Clear timeline

        GENERAL ADVICE:
        - Prevention + monitoring tips

        Important: 
        - This is not a diagnosis
        - Use simple, clear language
        """

        try:
            response = self.model.generate_content(prompt)
            return self._format_response(self._extract_text(response))
        except Exception as e:
            return (
                "I apologize, I'm having trouble processing your request. "
                "Please try again soon.\n\n"
                f"Technical details: {str(e)}"
            )
    
    def _extract_text(self, response):
        """Safely extract text from Gemini response."""
        try:
            if hasattr(response, 'text') and response.text:
                return response.text
            if response.candidates:
                return response.candidates[0].content.parts[0].text
        except:
            pass
        return "Sorry, I could not understand the response."
    
    def _format_response(self, text):
        lines = text.replace("**", "").split("\n")
        cleaned = [line.strip() for line in lines if line.strip()]

        final = "\n\n".join(cleaned)
        return final
  

    


