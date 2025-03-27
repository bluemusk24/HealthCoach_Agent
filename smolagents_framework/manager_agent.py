from exercise_agent import create_exercise_agent
from food_agent import create_food_agent
import asyncio
import os
from smolagents import CodeAgent, tool, HfApiModel
from typing import List, Dict, Any
from dotenv import load_dotenv, find_dotenv

# load the .env file
_ = load_dotenv(find_dotenv())
hf_token = os.getenv("HF_TOKEN")


@tool
def generate_workout_plan(goal: str) -> List[Dict[str, Any]]:
    """
    Generate a concise workout plan based on the need of the user.
    Args:
        goal: the reason for the workout by the user.
    """
    if goal.lower() == 'build muscle':
        exercises = create_exercise_agent('biceps')
    elif goal.lower() == 'lose weight':
        exercises = create_exercise_agent('cardio')
    else:
        exercises = create_exercise_agent('full body')
    return exercises[:5]    # Return top 5 exercises

@tool
def generate_meal_plan(dietary_preference: str) -> List[Dict[str, Any]]:
    """
    Generate a meal plan based on dietary preference.
    Args:
        dietary_preference: prefered diet for the user
    """
    foods = create_food_agent(dietary_preference)
    return foods[:5]

# Delegate task to this agent by manager_agent if it's fitness related
managed_exercise_agent = CodeAgent(
    tools=[generate_workout_plan],
    model=HfApiModel(),
    name="exercise_agent",
    description="This agent retrieves exercise routines" 
)

# Delegate task to this agent by manager_agent if it's food related
managed_food_agent = CodeAgent(
    tools=[generate_meal_plan],
    model=HfApiModel(),
    name="food_agent",
    description="This agent searches for food products"
)

# Manager Agent with Smolagents's Framework
def create_manager_agent():
    """
    Manager agent that delegates tasks to either food agent or exercise agent 
    """
    manager_agent = CodeAgent(    
        tools=[generate_workout_plan, generate_meal_plan],
        model=HfApiModel(),  #model_id='Qwen/Qwen2.5-7B-Instruct'
        managed_agents=[managed_exercise_agent, managed_food_agent]
    )
    return manager_agent



# for testing manager_agent locally. # the manager_agent function above and run:
#def main():

#    manager_agent = CodeAgent(
#        tools=[generate_workout_plan, generate_meal_plan],
#        model=HfApiModel(),
#        managed_agents=[managed_exercise_agent, managed_food_agent]
#    )
#    manager_agent.run(input("Enter Prefered Diet OR Fitness Plan: "))

#if __name__ == "__main__":
#    main()
