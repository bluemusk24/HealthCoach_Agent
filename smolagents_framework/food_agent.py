import asyncio
import requests
import os
from smolagents import CodeAgent, tool, HfApiModel
from typing import List, Dict, Any
from dotenv import load_dotenv, find_dotenv

# load the .env file
_ = load_dotenv(find_dotenv())
hf_token = os.getenv("HF_TOKEN")

BASE_URL = "https://world.openfoodfacts.org/api.v0/product"

# Tool decorator function to get food via barcode
@tool
def get_food_by_barcode(barcode: str) -> Dict[str, Any]:
    """
    Retrieve food product information by barcode from the Open Food Facts database.
    Args:
        barcode (str): The barcode of the food product to lookup
    """
    response = requests.get(f"{BASE_URL}/{barcode}.json")
    if response.status_code == 200:
        return response.json()
    return None

# Asynchronous tool decorator function to handle multiple food requests concurrently from users.
@tool
async def async_search_foods(query: str) -> List[Dict[str, Any]]:
    """
    Search for food products asynchronously from the Open Food Facts database. 
    Args:
        query (str): The search term for food products.
    """
    response = await asyncio.to_thread(
        requests.get, f"https://openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&json=1"
    )
    if response.status_code == 200:
        return response.json().get('products', [])
    return []

# Food Agent function
def create_food_agent(dietary_preference):
    """
    AI Agent that uses food search tools to retrieve food products.
    Args:
        dietary_preference: The dietary preference to search
    """
    food_agent = CodeAgent(
        tools=[get_food_by_barcode, async_search_foods],
        model=HfApiModel()
    )
    result = food_agent.run(f"Find food options for {dietary_preference} diet")
    return result


# for testing food_agent locally. # the create_food_agent function above and run:
#def main():
#    food_agent = CodeAgent(
#        tools=[get_food_by_barcode, async_search_foods],
#        model=HfApiModel()
#    )
#    food_agent.run(input("Enter your Dietary Preference: "))

#if __name__ == "__main__":
#    main()
