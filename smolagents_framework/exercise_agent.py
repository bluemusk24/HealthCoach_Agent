from diskcache import Cache
import requests
import os
from smolagents import CodeAgent, tool, HfApiModel
from typing import List, Dict, Any
from dotenv import load_dotenv, find_dotenv

# load the .env file
_ = load_dotenv(find_dotenv())
hf_token = os.getenv("HF_TOKEN")

BASE_URL = "https://exercisedb-api.vercel.app/api/exercises"
cache = Cache('./cache_dir')


# Tool decorator to get exercises by target muscle with caching
@tool
def get_exercises_by_target(target: str) -> List[Dict[str, Any]]:
    """
    Retrieves recommended exercise routine based on the target muscle group. 
    Args:
        target: muscle group for my workout routine
    """
    if target in cache:
        return cache[target]
    
    response = requests.get(f"{BASE_URL}/target/{target}")
    if response.status_code == 200:
        result = response.json()
        cache[target] = result     # Store result in cache
        return result
    return []                       # Return empty list if request fails


# Tool decorator to get exercises by equipment
@tool
def get_exercises_by_equipment(equipment: str) -> List[Dict[str, Any]]:
    """
    Retrieves recommended exercise routine based on required equipment. 
    Args:
        equipment: necessary equipment for my workout routine
    """
    response = requests.get(f"{BASE_URL}/equipment/{equipment}")
    if response.status_code == 200:
        return response.json()
    return []                      

# Exercise agent function
def create_exercise_agent(target_muscle):
    """
    AI Agent that retrieves exercise routines.
    Args:
        target_muscle: The target muscle to get exercises
    """
    exercise_agent = CodeAgent(
        tools=[get_exercises_by_target, get_exercises_by_equipment],
        model=HfApiModel()
    )
    result = exercise_agent.run(f"Get exercises for {target_muscle}")
    return result


# for testing exercise_agent locally. # the create_exercise_agent function above and run:
#def main():

#    exercise_agent = CodeAgent(
#        tools=[get_exercises_by_target, get_exercises_by_equipment],
#        model=HfApiModel()
#    )
#    exercise_agent.run(input("Enter your Fitness Goal: "))

#if __name__ == "__main__":
#    main()