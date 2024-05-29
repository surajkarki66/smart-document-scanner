FROM python:latest

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . .

# Install OpenCV dependencies
RUN apt-get update && \
    apt-get install -y libsm6 libxext6 libxrender-dev tesseract-ocr

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV using pip
RUN pip install opencv-python-headless

# Command to run the Flask application
CMD ["gunicorn", "app:create_app()", "--bind=0.0.0.0"]
