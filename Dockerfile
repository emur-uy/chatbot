# Start from the official Python 3 image
FROM python:3

# Set the working directory in the Docker image
WORKDIR /usr/src/app

# Copy requirements.txt into the Docker image
COPY requirements.txt ./

# Install the Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the Docker image
COPY . .

# Set environment variables
ENV PORT 5000
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Give execution permissions to startup.sh and set it as the command to run when the Docker container starts
RUN chmod +x startup.sh
CMD ["./startup.sh"]

