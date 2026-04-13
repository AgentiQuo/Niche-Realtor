from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import niche, property, neighborhood, client, match, intelligence_routes
from config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)



# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(niche.router, prefix="/niche", tags=["Niche"])
app.include_router(intelligence_routes.router, prefix="/niche", tags=["Niche Intelligence"])
app.include_router(property.router, prefix="/property", tags=["Property"])
app.include_router(neighborhood.router, prefix="/neighborhood", tags=["Neighborhood"])
app.include_router(client.router, prefix="/client", tags=["Client"])
app.include_router(match.router, prefix="/match", tags=["Match"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Niche Realtor API"}
