#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for PostgreSQL to start..."
until PGPASSWORD=password psql -h db -U user -d moviedb -c '\q'; do
  sleep 1
done
echo "PostgreSQL started"

# Run the add_sample_movies.py script automatically
echo "Adding sample movies to database..."
python add_sample_movies.py --auto-accept

# Start the FastAPI application
echo "Starting FastAPI application..."
exec "$@"