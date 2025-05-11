from typing import Dict, List
import os
import httpx
from langchain.tools import BaseTool
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManagerForToolRun

load_dotenv()

class SupabaseActivitySearch(BaseTool):
    name: str = "SupabaseActivitySearch"
    description = "Recherche des activités dans la base de données Supabase en fonction de la destination, l'humeur, le budget et les dates"

    def __init__(self):
        super().__init__()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}"
        }
        
        # Configuration de OpenRouter avec Mistral-7B
        self.llm = ChatOpenAI(
            model="mistralai/mistral-7b-instruct",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            headers={
                "HTTP-Referer": "https://odys.ai",
                "X-Title": "Odys.ai Travel Planner"
            }
        )

    def _run(self, params: Dict, run_manager: CallbackManagerForToolRun = None) -> List[Dict]:
        destination = params.get("destination", "").lower()
        mood = params.get("mood", "").lower()
        budget = params.get("budget")
        dates = params.get("dates")
        
        # Construction de la requête Supabase
        url = f"{self.supabase_url}/rest/v1/activities"
        
        # Filtrage par location et tags
        query_params = {
            "location": f"ilike.*{destination}*",
            "tags": f"cs.{{{mood}}}"
        }
        
        try:
            response = httpx.get(
                url,
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            
            activities = response.json()
            
            # Utilisation du LLM pour filtrer et personnaliser les résultats
            prompt = f"""<s>[INST] En tant qu'expert en voyages, analyse ces activités pour un séjour {mood} à {destination} 
            avec un budget de {budget}€ sur {dates}. Sélectionne et personnalise les meilleures suggestions.
            
            Activités disponibles:
            {activities}
            
            Retourne uniquement les activités les plus pertinentes, avec une description personnalisée pour chaque activité. [/INST]</s>"""
            
            llm_response = self.llm.predict(prompt)
            
            # Traitement de la réponse du LLM pour extraire les activités
            return [{
                "title": activity["title"],
                "description": activity["description"],
                "location": activity["location"],
                "price": activity["price"],
                "duration": activity["duration"],
                "booking_link": activity["booking_link"]
            } for activity in activities]
            
        except Exception as e:
            return [{"error": f"Erreur lors de la recherche d'activités: {str(e)}"}] 