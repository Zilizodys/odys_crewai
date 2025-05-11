from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from crewai import Crew
from agents.travel_planner import create_travel_planner_agent

app = FastAPI(title="Odys.ai Travel Planner API")

class TravelRequest(BaseModel):
    destination: str
    mood: str
    budget: Optional[float] = None
    dates: Optional[str] = None

class Activity(BaseModel):
    title: str
    description: str
    location: str
    price: float
    duration: str
    booking_link: str

@app.post("/generate", response_model=List[Activity])
async def generate_travel_plan(request: TravelRequest):
    try:
        # Création de l'agent
        travel_planner = create_travel_planner_agent()
        
        # Création du crew
        crew = Crew(
            agents=[travel_planner],
            tasks=[],
            verbose=True
        )
        
        # Préparation des paramètres pour la recherche
        search_params = {
            "destination": request.destination,
            "mood": request.mood,
            "budget": request.budget,
            "dates": request.dates
        }
        
        # Exécution de la recherche via l'agent
        result = travel_planner.execute_task(
            f"Trouve des activités à {request.destination} qui correspondent à une ambiance {request.mood}",
            search_params
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 