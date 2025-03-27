# PROJECTS DEFINITION:

* The aim of this project is to build a ```HEALTH COACH AGENTIC AI-Powered Application``` using [Smolagents Framework](https://huggingface.co/learn/agents-course/unit2/smolagents/introduction). The ```Health Coach AI Agent``` will be optimized, dockerized for deployment, and manage its operations effectively for scalability and reliability.

***Description*** : This agent provides users with workout and meal plans based on their fitness goals and dietary preferences in real time. This agent uses several ```APIs```, and integrates ```Gradio``` for an interactive and user-freindly experience. Reference Link: [Exercise_Database_API](https://exercisedb-api.vercel.app/docs).

## PROCEDURES:

* create a directory and virtual environment to separate dependencies.

```bash
mkdir HealthCoach_Agent

cd HealthCoach_Agent

conda create -n health_coach_agent python=3.11

conda activate health_coach_agent
```

* create a requirements.txt file for installation of necessary requirements for this applocation.

```bash
touch requirements.txt

pip install -r requirements.txt
```

* ```cache_dir``` - to store and retrieve cached data. It automatically handles writing to disk while keeping frequently accessed data in memory for speed. Also, it eliminates redundant API calls, and speeds up responses to frequently queried targets.

* [exercise_agent.py]() - an agent that interacts with an ```Exercise_Database_API```. The agent retrieves recommended workout routine based on ```target muscle``` group or required ```equipment```.

* .env - to load api keys.

* Test the ```exercise_agent``` locally:
```bash
python3 smolagents_framework/exercise_agent.py

Enter your Fitness Goal: lose weight, build muscle
```

* [food_agent.py]() - an agent that interact with a ```Food_Database_API```. The agent retrieves details about food items or search for foods (diet preferences) based on user inputs.

* Test the ```food_agent``` locally:
```bash
python3 smolagents_framework/food_agent.py

Enter your Dietary Preference: Low Carb, Vegan
```

* [manager_agent]() - a manager agent that delegates task to the ```exercise_agent``` or ```food_agent```

* Test the ```manager_agent``` locally:
```bash
python3 smolagents_framework/manager_agent.py

Enter Prefered Diet OR Fitness Plan: I want to build muscle
```

* [agent_main.py]() - agentic python script to tie the entire system together using ```Gradio``` to create an interactive user interface.

***Run this script***
```bash
python3 health_coach_agent/main_agent.py
```

***Results:***
1. Running on local URL: ```http://127.0.0.1:7860/``` - Gradio UI for seamless interaction. To create a public link, set `share=True` in `launch()`.
2. ```http://localhost:8000/``` - Prometheus UI to monitor request_processing_seconds_count 1.0
3. Check [health_coach.log]() for updated logs.

###  Deploying Health Coach Smolagent AI Agent With Docker

***create the following:***

* [docker_agent.py]() - python script to include an environment variable for ```Gradio```.

* [Dockerfile]() - to build a docker image and containerized our application to enable deployment. Run codes below:
```bash
docker build -t health_coach_smolagent:v1 .

docker run -it --rm -p 7860:7860 health_coach_smolagent:v1
```

```http://localhost:7860/``` - Launch Gradio UI for seamless interaction. To create a public link, set `share=True` in `launch()`.

***Pictorial View of Gradio:*** [Gradio_Image]()

* [locust_agent.py]() - python script to observe and simulate a large number of users interacting with the application concurrently, test app's scalability and reliability. Wait time is around 1-2 seconds for virtual users' post request to the application endpoint. 

* Run code below to load test our application with 10 users at a rate of 10 requests/sec.

```bash
locust -f locust_agent.py --host http://localhost:7860
```
***Result:*** Launch Locust web interface at ```http://localhost:8089```

***Pictorial View of Locust:*** [Locust_Image]()

### Tracing Smolagents (Health_Coach Agent) with Arize Phoenix

* [agent_arize_tracing.py]() - python script to log in traces, monitor and evaluate agents with [ARIZE_PHOENIX](https://phoenix.arize.com/)
```bash 
python3 agent_arize_tracing.py
```
[PhoenixArize_Tracing1]() [PhoenixArize_Tracing2]()


## Tech Stack:
***Gradio*** - to create a seemless user interface.
***Prometheus*** - to monitor systems performance by tracking how long each user request takes to process.
***Locust*** - python-based-load-testing framework for performance of APIs.
***Smolagents*** - huggingface agentic framework to build AI agents.


* ```main_agent.py``` code for JSON output in Gradio UI

```bash
import gradio as gr
from manager_agent import create_manager_agent
from loguru import logger
from prometheus_client import start_http_server, Summary
import json

# Error and Debug logs are added to track issues
logger.add("health_coach.log", rotation="1 MB")

# Prometheus server to collect metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Timing function for Prometheus
@REQUEST_TIME.time()  
def health_coach(goal, dietary_preference):
    """
    Handles both workout and meal plan generation.
    """
    try:
        logger.info(f"Workout routine for goal: {goal} and diet: {dietary_preference}")
        manager = create_manager_agent()

        # Get workout plan and meal plan
        workout_plan_result = manager.run(f"Create a workout plan for {goal}")
        logger.info(f"Generated workout plan: {type(workout_plan_result)}")

        meal_plan_result = manager.run(f"Create a meal plan for {dietary_preference}")
        logger.info(f"Generated meal plan: {type(meal_plan_result)}")

        # Parse workout plan and meal plan as JSON; if fails, use the string representation
        try:
            workout_plan = json.loads(str(workout_plan_result))
        except json.JSONDecodeError:
            workout_plan = {"result": str(workout_plan_result)}
            
        try:
            meal_plan = json.loads(str(meal_plan_result))
        except json.JSONDecodeError:
            meal_plan = {"result": str(meal_plan_result)}

        logger.info(f"Processed workout plan: {type(workout_plan)}")
        logger.info(f"Processed meal plan: {type(meal_plan)}")
        
        return workout_plan, meal_plan
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.exception("Full traceback:")
        return {"error": str(e)}, {"error": str(e)}
    
# Gradio app
app = gr.Interface(
    fn=health_coach,
    inputs=[
        gr.Textbox(label="Fitness Goal (e.g., Build Muscle, Lose Weight)"),
        gr.Textbox(label="Dietary Preference (e.g., Vegan, Low Carb)")
    ],
    outputs=[
        gr.JSON(label="Personalized Workout Plan"),
        gr.JSON(label="Personalized Meal Plan"),
    ],
    title="Personal Health Coach AI Agent",
    description="Enter your fitness goal and dietary preference to receive personalized workout and meal plans"
)

def main():
    # Start Prometheus metrics server and launch Gradio app
    start_http_server(8000)   
    app.launch(share=True)     

if __name__ == "__main__":
    main()
```