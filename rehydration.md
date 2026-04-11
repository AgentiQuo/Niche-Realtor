# 🧊 **NICHE REALTOR — FULL PLATFORM REHYDRATION SPEC**  
**Version**: 1.0.0  
**Status**: Production-Ready / Backend Deployed  
**Platform Scope**: Full-Stack (Next.js + FastAPI + AI Agents)

---

## **1. BACKEND ARCHITECTURE (The Engine)**

The Niche Realtor backend is a high-performance, deterministic API built with **FastAPI**. It is designed to be "Agent-Friendly," meaning it uses strict types, clear endpoints, and structured responses that LLMs can easily interpret and interact with.

### **Modular Folder Structure**
All Python code resides in the `backend/` directory to ensure Railway compatibility:
- **`routes/`**: Endpoint definitions and request/response routing.
- **`services/`**: Core business logic. No specialized logic lives in routes.
- **`models/`**: Pydantic schemas. Distinct separation between Public models (API) and Internal models (Persistence).
- **`db/`**: Repository layer using `relational_db` (In-memory/Postgres) and `vector_db` (Cosine similarity storage).
- **`embeddings/`**: Vector math, normalization, and embedding generation logic.
- **`agents/`**: Autonomous AI agents that utilize the service layer for orchestration.

### **The Tag System (Refactored)**
- **Public Request**: Simple inline objects `{"name": "string"}`.
- **Internal Reality**: Server-side logic promotes these to `TagInternal` models, adding `tag_id`, `polarity`, `relevance`, and `embeddings`.
- **Response Privacy**: Internal metadata is stripped during JSON serialization, keeping the public API clean.

### **Intelligence Layer**
- **Semantic Search**: Text-to-vector conversion followed by vector ranking.
- **Similarity Engine**: Cold-start compatible similarity based on shared tag/neighborhood embeddings.
- **Matching Engine**: Cross-references client profiles with niche vectors using the `MatchingEngineAgent`.

### **Deployment Invariants**
- Deployed on **Railway**.
- Entry point: `backend/main.py`.
- Must execute from `backend/` directory context for module resolution.

---

## **2. FRONTEND ARCHITECTURE (The Interface)**

### **Framework: Next.js (App Router)**
- **Why**: Excellent SEO for real estate listings, fast server-side rendering (SSR) for property details, and a first-class deployment experience on Vercel.
- **Styling**: Vanilla CSS or Tailwind (based on specific user preference), emphasizing glassmorphism and modern UI.

### **Architectural Patterns**
- **API Client Generation**: The frontend uses standard tools to generate a TypeSafe client directly from the backend's `/openapi.json`.
- **Pages**:
    - `/niches`: Dashboard and listing.
    - `/niches/[id]`: Deep dive into niche tags, neighborhoods, and matched properties.
    - `/create`: Guided niche creation flow with real-time tag suggestions.
    - `/search`: Semantic search bar with result preview.
- **Deployment**: **Vercel** with automatic PR previews.

---

## **3. THE AGENT LAYER (Autonomous Intelligence)**

Agents are the "workers" of the platform. They don't just process data; they reason.

- **Matching Engine Agent**: Interprets complex client profiles (e.g., "Family moving from NYC with 2 dogs") and maps them to niche embeddings.
- **Listing Scraper Agent**: Ingests raw property data and extracts structured tags (e.g., "mid-century modern", "proximity to schools").
- **Client Modeling Agent**: Analyzes user behavior to refine the "Client Profile" vector dynamically.
- **Neighborhood Scout Agent**: Correlates demographic and crime data into "Vibe Tags" for neighborhoods.

**Agent Reasoning Loop**:
1. Agent receives a Trigger (e.g., "New Property Ingested").
2. Agent calls `embedding_service` to represent the data.
3. Agent uses the `relational_db` to fetch context.
4. Agent writes its conclusions (Tags/Scores) back to the system.

---

## **4. INTELLIGENCE & VECTOR MATH**

- **Embedding Construction**: 
    - `niche_vector = normalize(sum(tag_vectors) + sum(neighborhood_vectors))`.
- **Similarity Comparison**: Standardized **Cosine Similarity**.
- **Vector Space**: Fixed-size vectors (default 1536) ensuring compatibility across all models.
- **Search Logic**: Every "Niche" is stored in the `vector_db` with its metadata, allowing for sub-millisecond similarity lookups across the entire database.

---

## **5. STEP-BY-STEP REHYDRATION PLAN**

| Phase | Description | Why It Matters | Output |
| :--- | :--- | :--- | :--- |
| **1. BE Bootstrapping** | Setup FastAPI, Folder Structure, and Railway config. | Foundational stability. | Healthy `/` endpoint. |
| **2. Tag Refactor** | Move to inline tag creation with `TagInternal` promotion. | Simplifies UX while keeping BE robust. | Success in `/niche/create`. |
| **3. Intelligence Layer** | Implement `/search`, `/similar`, and `/match`. | Adds the unique semantic value. | Ranked JSON results. |
| **4. FE Scaffolding** | Create Next.js app and generate API Client. | Bridges code to visuals. | Functional API calls in UI. |
| **5. Core UI CRUD** | Build Niche List, Create, and Detail pages. | Enables human data entry. | Full niche management loop. |
| **6. Intelligence UI** | Build the Search bar and Similarity carousels. | Surface AI capabilities to users. | "Wowed" user experience. |
| **7. Agent Integration** | Connect Scraper and Matcher agents to live services. | Enables automation. | Autonomous property tagging. |
| **8. Final QA** | End-to-end testing of Railway-to-Vercel flow. | Ensures production readiness. | Zero-error production build. |

---

## **6. DEFINITION OF DONE (DoD)**

The platform is officially rehydrated when:
1. [ ] **Backend** is live on Railway with zero import errors.
2. [ ] **Frontend** is live on Vercel and communicates with the Backend.
3. [ ] **Inline Tags** can be created during Niche creation without providing IDs.
4. [ ] **Search** returns niches by meaning, not just keywords.
5. [ ] **Similar Niches** show relevant matches with score percentages.
6. [ ] **Matching Flow** can take a raw JSON profile and return ranked results.
7. [ ] **Full Documentation** (OpenAPI) reflects all available endpoints.
8. [ ] **Test Suite** confirms that internal tag metadata is never leaked to the frontend.

---
**END OF SPEC**
