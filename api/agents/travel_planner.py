from crewai import Agent
from tools.supabase_tool import SupabaseActivitySearch

def create_travel_planner_agent():
    return Agent(
        role="Expert en planification de séjours personnalisés",
        goal="Générer des suggestions d'activités pertinentes et personnalisées pour les voyageurs",
        backstory="""Vous êtes un expert en planification de voyages avec une connaissance approfondie 
        des destinations et des activités touristiques. Votre mission est d'aider les voyageurs à 
        découvrir les meilleures expériences adaptées à leurs préférences.""",
        tools=[SupabaseActivitySearch()],
        verbose=True
    ) 