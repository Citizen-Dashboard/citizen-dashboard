# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files for installing dependencies
COPY poetry.lock pyproject.toml /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY . /app/

# Copy initialization and data files
COPY items_data.csv /app/
COPY populate_db.py /app/

# Expose the port the app runs on
EXPOSE ${SEARCH_API_PORT}

# Run the application
CMD ["python", "search_api.py"]
