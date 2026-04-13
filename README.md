# Niche Realtor — Full Platform (Rehydrated)

Niche Realtor is a multi‑agent, AI‑native real‑estate intelligence system.

## 🚀 Canonical Architecture
As per the Rehydration Spec, this repository follows a strict deployment-ready structure:

- **`/backend`**: The FastAPI engine (Deployed on Railway).
  - `/agents`: Autonomous reasoning loop agents.
  - `/routes`: Endpoint definitions.
  - `/services`: Business logic & agent orchestration.
  - `/models`: Pydantic schemas (Public & Internal).
  - `/db`: Persistence layer (In-memory/Supabase).
  - `/embeddings`: Vector math & embedding construction.
  - `/config`: Environment settings.
- **`/frontend`**: The Next.js / React interface (Deployed on Vercel).

## 🧊 Global Rehydration Rules (Deterministic)
1. **No sibling Python folders**: All Python code must be in `backend/`.
2. **Environment Controlled**: Configuration is driven by `backend/config/settings.py`.
3. **Agent First**: All complex reasoning lives in the agent layer, exposed via services.

## 🛠️ Getting Started

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Seed & Integration
Run `seed_integration.py` from the root (ensuring the backend is running) to populate the platform with initial test data.
