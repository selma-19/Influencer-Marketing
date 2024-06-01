FROM python:3.12-slim
#LABEL authors="wawao"


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .. /app

RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
#ENTRYPOINT ["top", "-b"]

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME InfluencerMarketingModel

# Run app.py when the container launches
CMD ["python", "app.py"]