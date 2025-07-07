# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for PDF generation
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir openai fpdf markdown xhtml2pdf flask flask_cors beautifulsoup4 requests

# Copy all project directories into the container
COPY Ai_Resume/ /app/Ai_Resume/
COPY Course_scraper/ /app/Course_scraper/
COPY Ui_api/ /app/Ui_api/

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Default command: run the UI API
CMD ["python", "Ui_api/skill_gap_api.py"]

 