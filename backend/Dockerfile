FROM python:3.10-slim

WORKDIR /app

# Install PostgreSQL client for the wait script
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Expose the port that FastAPI runs on
EXPOSE 8000

# Use our entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Command to run the FastAPI application
CMD ["uvicorn", "main_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]