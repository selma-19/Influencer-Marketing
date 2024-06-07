FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /flask

# Copy the current directory contents into the container at /app
COPY . /flask

# Install Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++
RUN pip install --no-cache-dir -r requirements.txt

# Download the spacy model
RUN python -m spacy download en_core_web_sm

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]