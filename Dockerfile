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

# Declare arguments which will be passed via --build-arg
ARG ENVIRONMENT

ARG SECRET_KEY
ARG APP_CLIENT_ID
ARG OPENAPI_CLIENT_ID
ARG TENANT_ID
ARG GRAPH_SECRET
ARG CLIENT_SECRET

ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# Set the environment variables
ENV ENVIRONMENT=$ENVIRONMENT

ENV SECRET_KEY=$SECRET_KEY
ENV APP_CLIENT_ID=$APP_CLIENT_ID
ENV OPENAPI_CLIENT_ID=$OPENAPI_CLIENT_ID
ENV TENANT_ID=$TENANT_ID
ENV GRAPH_SECRET=$GRAPH_SECRET
ENV CLIENT_SECRET=$CLIENT_SECRET

ENV POSTGRES_SERVER=$POSTGRES_SERVER
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

# Command to run the application
CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Make port 80 available to the world outside this container for azure container registry port
EXPOSE 80
