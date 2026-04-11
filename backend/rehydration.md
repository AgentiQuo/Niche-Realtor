
# ✅ **FULL REHYDRATION FILE (PRODUCTION‑SAFE)**  
Copy/paste this exactly as-is into Antigravity when rehydrating. This was made just after the backend was deployed.

---

## **SYSTEM STATE — NICHE REALTOR PLATFORM (BACKEND DEPLOYED)**

### **1. Deployment Architecture (Final, As‑Deployed)**  
- **Backend**: FastAPI app deployed on **Railway**  
- **Frontend**: Will be deployed on **Vercel**  
- **Database**: Supabase (PostgreSQL + vector extension)  
- **Backend entrypoint**: `backend/main.py`  
- **Backend root directory**: `backend/`  
- **Python version**: 3.13.x (Railway environment)  
- **Public backend URL**:  
  `https://meticulous-comfort-production-ce41.up.railway.app`

### **2. Hard Deployment Invariants (MUST NEVER CHANGE)**  
These rules prevent the import‑path failures we fixed during deployment.

- **All Python code MUST live inside the `backend/` folder.**  
- **No Python modules may exist at the repo root.**  
- **No imports may reference modules outside `backend/`.**  
- **Agents must live in `backend/agents/`.**  
- **Embeddings must live in `backend/embeddings/`.**  
- **Routers must live in `backend/routes/`.**  
- **Services must live in `backend/services/`.**  
- **Models/schemas must live in `backend/models/`.**  
- **The backend folder is the ONLY deployable Python context.**  
- **Railway deploys from the repo root but executes from `backend/`.**  
- **Relative imports must be backend‑internal (e.g., `from routes.x import y`).**  
- **No top‑level Python files outside `backend/`.**  
- **No sibling folders containing Python code.**  
- **No dynamic path manipulation.**  
- **No absolute imports referencing the old structure.**

These invariants ensure Railway will always find the modules.

### **3. Backend Folder Structure (Canonical)**  
This is the **exact** structure Antigravity must preserve:

```
backend/
    main.py
    routes/
        niche.py
        property.py
        client.py
        neighborhood.py
        match.py (if exists)
    services/
        niche_service.py
        property_service.py
        client_service.py
        neighborhood_service.py
        match_service.py
    models/
        niche.py
        property.py
        client.py
        neighborhood.py
        match.py
        shared.py
    agents/
        <all agent modules>
    embeddings/
        <embedding logic, vector utils, similarity functions>
    utils/
        <helpers, logging, config>
    config/
        settings.py (Supabase URL, keys, env vars)
```

### **4. Router Registration (Required in main.py)**  
Antigravity must always ensure `main.py` includes:

```python
from fastapi import FastAPI
from routes.niche import router as niche_router
from routes.property import router as property_router
from routes.client import router as client_router
from routes.neighborhood import router as neighborhood_router
# optional:
# from routes.match import router as match_router

app = FastAPI()

app.include_router(niche_router, prefix="/niche")
app.include_router(property_router, prefix="/property")
app.include_router(client_router, prefix="/client")
app.include_router(neighborhood_router, prefix="/neighborhood")
# optional:
# app.include_router(match_router, prefix="/match")
```

This ensures all endpoints appear in `/docs`.

### **5. Current Backend State (Verified)**  
- Server boots cleanly  
- No import errors  
- No missing modules  
- `/docs` loads  
- Root GET (`/`) works  
- POST endpoints appear  
- GET list endpoints return `[]` (empty DB)  
- No runtime crashes  
- CORS not yet tested  
- DB is empty (expected)  

### **6. Agentic Orchestration Rules (Deterministic)**  
- Agents live in `backend/agents/`  
- Agents may call services but not vice‑versa  
- Agents may call embeddings utilities  
- Agents must not import from outside `backend/`  
- Agents must not modify folder structure  
- Agents must not create new top‑level modules  
- Agents must not create new root‑level folders  
- Agents must not assume local filesystem beyond backend/  

### **7. Embeddings & Vector Logic Rules**  
- All embedding logic lives in `backend/embeddings/`  
- Vector similarity functions live here  
- No external file paths  
- No absolute imports  
- No top‑level scripts  

### **8. Supabase Integration Rules**  
- Environment variables must be read from Railway  
- No hardcoded keys  
- No local `.env` assumptions  
- All DB access goes through service layer  
- No direct DB access from routers  

### **9. Frontend Integration Expectations**  
- Frontend will call backend via the public URL  
- CORS must allow Vercel domain  
- JSON bodies must match Pydantic schemas  
- POST endpoints will be triggered by UI flows  
- GET endpoints will be used for listing  

### **10. Next‑Phase Tasks (Not yet executed)**  
- Deploy frontend  
- Connect frontend to backend  
- Test CORS  
- Create first niche/property/client  
- Run first match  
- Populate DB  
- Validate agentic workflows end‑to‑end  

### **11. Antigravity Behavioral Constraints**  
When generating or modifying code:

- MUST preserve folder structure exactly  
- MUST preserve import boundaries  
- MUST not create new root‑level Python files  
- MUST not propose restructuring  
- MUST not move agents or embeddings  
- MUST not introduce circular imports  
- MUST not generate code outside backend/  
- MUST not assume local execution environment  
- MUST generate Railway‑compatible imports  
- MUST maintain deterministic architecture  

### **12. Purpose of This Rehydration File**  
This file rehydrates the system into the **exact state** of the deployed backend so Antigravity can:

- reason correctly  
- avoid drift  
- avoid restructuring  
- avoid breaking imports  
- avoid breaking deployment  
- expand safely  
- generate new modules without breaking the architecture  

---

# 🎉 **Your rehydration file is complete.**

This is the safest, most deterministic version — Antigravity will not go off‑track when you paste this.

When you're ready to continue later, just say the word and we’ll test the backend through the frontend.
