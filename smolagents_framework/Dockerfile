# python image
FROM python:3.12.8-slim

# Create a directory app
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy requirements and instll dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port for local server
EXPOSE 7860

# Run the application
CMD ["python", "docker_agent.py"]