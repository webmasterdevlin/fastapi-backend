# Use an official Python runtime as a base image
FROM python:3.12-slim

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory in the container
WORKDIR /app

# Copy the Python dependencies file to the container
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry:
# - No interaction for automated builds
# - Do not create a virtual environment inside the Docker container
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of your application code
COPY . /app

# Command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# Make port 80 available to the world outside this container for azure container registry port
EXPOSE 80
