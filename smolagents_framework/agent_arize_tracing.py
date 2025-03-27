import os
from dotenv import load_dotenv, find_dotenv
#from smolagents import CodeAgent, tool, HfApiModel
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from manager_agent import create_manager_agent

# load the .env file
_ = load_dotenv(find_dotenv())
phoenix_api_key = os.getenv("PHOENIX_API_KEY")
hf_token_value = os.getenv("HF_TOKEN")

# Set the environment variables with the provided keys
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={phoenix_api_key}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
os.environ["HF_TOKEN"] = f"{hf_token_value}"

def main():
    # Define the Trace Provider
    tracer_provider = register(project_name="Health-Coach-Agent")               #auto_instrument=True

    # Instrument Smolagents
    SmolagentsInstrumentor().instrument(tracer_provider=tracer_provider)

    manager = create_manager_agent()
    manager.run(input("Enter Prefered Diet OR Fitness Plan: "))

if __name__ == "__main__":
    main()