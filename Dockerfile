# Use a lightweight Alpine Linux image
FROM alpine:3.20

# Install necessary packages and Tesseract OCR
RUN apk update && apk upgrade && apk add --no-cache \
    tesseract-ocr \
    tesseract-ocr-data-eng \
    python3 \
    py3-pip \
    build-base \
    jpeg-dev \
    zlib-dev \
    libpng-dev \
    gcc \
    musl-dev \
    bash

# Set the working directory
WORKDIR /app

# Copy all files to the working directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Tesseract path in your environment variables
ENV TESSERACT_PATH=/usr/bin/tesseract

# Expose the port the app runs on
EXPOSE 5000

# Run the application using gunicorn
CMD ["gunicorn", "busimageparsing:app", "-b", "0.0.0.0:5000"]
