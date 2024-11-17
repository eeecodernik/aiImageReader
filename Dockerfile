# Use an official Python image as the base
FROM python:3.11-slim

# Install Tesseract OCR and its dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all the project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Tesseract path in your environment variables
ENV TESSERACT_PATH=/usr/bin/tesseract

# Expose the port your app runs on
EXPOSE 5000

# Start the application using gunicorn
CMD ["gunicorn", "busimageparsing:app", "-b", "0.0.0.0:5000"]
