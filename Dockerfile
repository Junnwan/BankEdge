# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory to /app
# Set the working directory to /app
WORKDIR /app

# Install system dependencies for Scikit-Learn (OpenMP) and others
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Train the ML model inside the container to ensure compatibility
# (Requires ml_data/ to be present in build context)
RUN python scripts/train_offloading_model.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run flask when the container launches
# Run app.py using Gunicorn
CMD ["gunicorn", "-w", "4", "--timeout", "120", "-b", "0.0.0.0:5000", "app:app"]
