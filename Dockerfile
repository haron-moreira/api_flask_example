
# Use the official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app


# Copy the application files to the container
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gunicorn && \
    rm -rf /var/lib/apt/lists/* \

RUN apt-get install gunicorn

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
# CMD ["python", "app.py"]
