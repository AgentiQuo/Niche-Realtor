import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def post_json(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def run_integration_tests():
    print("--- Phase 1: Niche Genesis ---")
    niche_payload = {
        "name": "Artist Lofts",
        "description": "Creative artist lofts with industrial vibes",
        "tags": [
            {
                "tag_id": "tag-1",
                "name": "Creative", 
                "polarity": "positive", 
                "relevance": 9.0,
                "confidence": 0.9,
                "source": "text",
                "embedding": [0.1] * 128
            },
            {
                "tag_id": "tag-2",
                "name": "Industrial", 
                "polarity": "positive", 
                "relevance": 8.5,
                "confidence": 0.85,
                "source": "text",
                "embedding": [0.15] * 128
            }
        ],
        "sources": []
    }
    resp = post_json(f"{BASE_URL}/niche/create", niche_payload)
    niche_id = resp.get("niche_id")
    print(f"Created Niche ID: {niche_id}")

    print("\n--- Phase 2: Property Ingestion Pipeline ---")
    prop_payload = {
        "url": "https://zillow.com/mock-artist-loft",
        "images": [],
        "metadata": {"price": 800000, "location": "Arts District"}
    }
    resp = post_json(f"{BASE_URL}/property/ingest", prop_payload)
    property_id = resp.get("property_id")
    print(f"Ingested Property ID: {property_id}")

    print("\nTriggering Property Analysis...")
    resp = post_json(f"{BASE_URL}/property/analyze", {"property_id": property_id})
    print("Property Analysis Result:", json.dumps(resp, indent=2))

    print("\n--- Phase 3: Client Journey ---")
    client_payload = {
        "preferences": {
            "budget": "$800k",
            "lifestyle": "Walkable"
        }
    }
    resp = post_json(f"{BASE_URL}/client/create", client_payload)
    client_id = resp.get("client_id")
    print(f"Created Client ID: {client_id}")

    print("\nSending Feedback Loop Adjustment...")
    feedback_payload = {
        "client_id": client_id,
        "feedback": {"liked": "Balcony"}
    }
    resp = post_json(f"{BASE_URL}/client/update", feedback_payload)
    print("Updated Client Embedding (length):", len(resp.get("updated_client_embedding", [])))

    print("\n--- Phase 4: Matching Engine ---")
    print("Executing Vector DB Search & Agent 5 Matching Logic...")
    match_payload = {
        "client_id": client_id,
        "niche_id": niche_id
    }
    resp = post_json(f"{BASE_URL}/match/", match_payload)
    print("Match Results:")
    print(json.dumps(resp, indent=2))
    
    with open("test_ids.json", "w") as f:
        json.dump({"niche_id": niche_id, "property_id": property_id, "client_id": client_id}, f)

    print("\nVerification Complete.")

if __name__ == "__main__":
    run_integration_tests()
