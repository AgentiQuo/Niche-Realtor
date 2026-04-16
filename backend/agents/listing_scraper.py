from typing import Dict, Any, List
from services.llm_service import llm_service_instance
from utils.agent_config import get_agent_config
import json

class ListingScraper:
    """
    Agent 1 — Listing Scraper
    Purpose: Convert raw listing sources into structured data.
    Input: URLs, HTML, PDFs, uploaded files
    Output: ListingObject (dictionary)
    """
    def __init__(self):
        self.config = get_agent_config("listing_scraper")

    def extract(self, source: str) -> Dict[str, Any]:
        """
        Uses an LLM to extract structured data from a raw source.
        In a real scenario, you might pass the HTML content here.
        """
        system_prompt = """
        You are a Real Estate Data Extraction specialist. 
        Extract structured information from the provided text or URL.
        Return ONLY valid JSON.
        """
        
        prompt = f"Please extract property details from this source: {source}. Include price, beds, baths, size_sqft, and location."
        
        response = llm_service_instance.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.config.get("model"),
            temperature=self.config.get("temperature", 0.1)
        )
        
        try:
            # Attempt to parse JSON from the LLM response
            # Note: In production you'd use a more robust parsing logic/library
            data = json.loads(response)
            return {
                "url": source,
                "images": [f"{source}/img1.jpg", f"{source}/img2.jpg"], # Images still mocked for now
                "metadata": data
            }
        except Exception:
            # Fallback if parsing fails or LLM gives text
            print("Failed to parse LLM response as JSON, returning formatted mock.")
            return {
                "url": source,
                "images": [f"{source}/img1.jpg", f"{source}/img2.jpg"],
                "metadata": {
                    "price": 0,
                    "beds": 0,
                    "baths": 0,
                    "size_sqft": 0,
                    "location": "Extraction Failed",
                    "raw_response": response
                }
            }

listing_scraper_agent = ListingScraper()
