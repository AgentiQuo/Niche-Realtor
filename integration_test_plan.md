# Niche Realtor — End-to-End Integration Test Plan

This integration test plan sequentially verifies the complete pipeline of the Niche Realtor application, guaranteeing that the Next.js Frontend, FastAPI Backend, Agent Operations, and In-Memory Vector Storage operate cohesively according to the BC specifications.

---

## Phase 1: Niche & Intelligence Genesis (Backend/Agent Logic)

**Test 1.1: Niche Creation (POST `/niche/create`)**
*   **Action**: Send a POST request to FastAPI with a sample niche payload (`name`: "Artist Lofts", `tags`: [{`name`: "Creative", `polarity`: "positive", `relevance`: 9.0...}]).
*   **Verification**: 
    1. HTTP 200 OK.
    2. Response includes a valid `niche_id`.
    3. *Backend integrity*: NicheService properly executed `compute_niche_embedding` algorithm and successfully stored the object in both `relational_db` and `vector_db`.

**Test 1.2: Neighborhood Intel (Frontend → Backend → Agent 3)**
*   **Action**: Navigate the Frontend to `/neighborhood/Arts-District`.
*   **Verification**:
    1. Network fires `POST /neighborhood/analyze` payload to FastAPI.
    2. Agent 3 (`NeighborhoodScoutAgent`) securely intercepts execution, mocking location analysis and generating polarity vectors.
    3. UI renders the successfully returned `vibe_summary`, styling "Walkable" and "Noisy" inside the colored `NicheTagCloud`.

---

## Phase 2: Property Ingestion Pipeline (Backend/Agent Logic)

**Test 2.1: Property Scraper (POST `/property/ingest`)**
*   **Action**: Fire an ingest route against `/property/ingest` with a mock Zillow URL.
*   **Verification**:
    1. HTTP 200 OK returning `property_id`.
    2. Agent 1 (`ListingScraper`) correctly intercepts the operation mapping "price" and "location" into structured JSON without hallucinating state.

**Test 2.2: Property Analysis (Frontend → Backend → Agent 2)**
*   **Action**: Navigate the Frontend to `/property/{property_id}` (using ID derived from Test 2.1).
*   **Verification**:
    1. Network fires `POST /property/analyze` dynamically.
    2. Agent 2 (`PropertyAnalysisAgent`) computes the vector sum mappings and assigns tags (e.g., "Spacious", "Natural Light").
    3. UI successfully loads identical tags in the UI alongside mapped Image strings.
    4. *System State*: `vector_db` validates the embedding insertion at DB level linking `{property_id}`.

---

## Phase 3: Client Journey & Preference Mapping

**Test 3.1: Client Onboarding (Frontend → Backend → Agent 4)**
*   **Action**: Open `/client` on the Frontend. Fill out the `ClientIntakeForm` (Budget: "$800k", Lifestyle: "Walkable"). Click "Generate Profile".
*   **Verification**:
    1. Network fires `POST /client/create`.
    2. Agent 4 computes the baseline vector from the payload and registers the state.
    3. Response delivers `client_id` to React.
    4. UI transitions gracefully to mount `ClientDashboard` hiding the intake form.

**Test 3.2: Feedback Loop Adjustment (POST `/client/update`)**
*   **Action**: Fire an update payload directly via cURL mapped to the newly created `client_id` with `feedback` = `{"liked": "Balcony"}`.
*   **Verification**:
    1. Backend `client_service` proxies request to Agent 4 `update_with_feedback`.
    2. Embedding math correctly parses adjustments via `normalize(base + adjustment)` math.
    3. HTTP 200 OK mapping `updated_client_embedding` floats.

---

## Phase 4: Matching Engine & Explanation Display (End-to-End Sequence)

**Test 4.1: Vector DB Search Execution**
*   **Action**: With NICHE_ID (Test 1.1), PROPERTY_ID (Test 2.1), and CLIENT_ID (Test 3.1) loaded into system state, navigate Frontend to `/match`.
*   **Verification**:
    1. Input `client_id` and `niche_id`, then click "Find Matches".
    2. `POST /match` is fired.

**Test 4.2: Matching Engine Logic (Agent 5)**
*   **Action**: Backend transfers routing payload to `MatchingEngineAgent`.
*   **Verification**:
    1. Agent 5 pulls client and niche abstractions from DB, fusing them mathematically correctly `c_vec + n_vec`.
    2. Agent iterates via `cosine_similarity` traversing *all* inserted properties (specifically asserting Test 2.1 exists and has a match score applied).
    3. Agent maps explicit `aligned_tags` context explanations.

**Test 4.3: Frontend UI Reconciliation**
*   **Action**: Return payload loads on the DOM.
*   **Verification**:
    1. `MatchResultsList.jsx` parses the array.
    2. A `PropertyCard.jsx` loads rendering the exact `% Match` numeric mapped from algorithmic cosine logic.
    3. `MatchExplanationBox.jsx` loads directly next to it containing dynamically rendered `[Natural Light]` UI spans generated completely end-to-end natively through the chain.
