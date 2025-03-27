import gradio as gr
from manager_agent import create_manager_agent
from loguru import logger
from prometheus_client import start_http_server, Summary
import os

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

        workout_plan = str(workout_plan_result)
        meal_plan = str(meal_plan_result)

        logger.info("Plans converted to readable text format")
        
        return workout_plan, meal_plan
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.exception("Full traceback:")
        return f"Error generating workout plan: {str(e)}", f"Error generating meal plan: {str(e)}"
    
# Gradio app
app = gr.Interface(
    fn=health_coach,
    inputs=[
        gr.Textbox(label="Fitness Goal (e.g., Build Muscle, Lose Weight)"),
        gr.Textbox(label="Dietary Preference (e.g., Vegan, Low Carb)")
    ],
    outputs=[
        gr.Textbox(label="Personalized Workout Plan", lines=10),
        gr.Textbox(label="Personalized Meal Plan", lines=10),
    ],
    title="Personal Health Coach AI Agent",
    description="Enter your fitness goal and dietary preference to receive personalized workout and meal plans"
)

def main():
    # Start Prometheus metrics server
    start_http_server(8000) 
    port = int(os.getenv("PORT", 7860))  # gradio port environment
    app.launch(server_name="0.0.0.0", server_port=port)     

if __name__ == "__main__":
    main()