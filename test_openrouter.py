import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def test_openrouter_connection():
    # Configuration de OpenRouter avec Mistral-7B
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Test simple avec Mistral-7B
    prompt = """<s>[INST] Tu es un expert en voyages. Donne-moi 3 suggestions d'activités romantiques à faire à Paris. [/INST]</s>"""
    
    try:
        response = llm.predict(prompt)
        print("✅ Connexion à OpenRouter réussie !")
        print("\nRéponse de Mistral-7B :")
        print(response)
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion à OpenRouter : {str(e)}")

if __name__ == "__main__":
    test_openrouter_connection() 