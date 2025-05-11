import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def test_supabase_connection():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}"
    }
    
    # Test de la connexion à la table activities
    url = f"{supabase_url}/rest/v1/activities"
    
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        
        activities = response.json()
        print(f"✅ Connexion à Supabase réussie !")
        print(f"Nombre d'activités trouvées : {len(activities)}")
        
        if activities:
            print("\nExemple d'activité :")
            print(activities[0])
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion à Supabase : {str(e)}")

if __name__ == "__main__":
    test_supabase_connection() 