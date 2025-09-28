# SnapStudio Docker Image
# Professional Photography Business Management System

FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=web_app.py \
    FLASK_ENV=production \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5001

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libc6-dev \
        libffi-dev \
        libssl-dev \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs backups exports uploads temp

# Set permissions
RUN chmod +x *.py

# Create non-root user for security
RUN groupadd -r snapstudio && useradd -r -g snapstudio snapstudio

# Ensure data directory is writable by the snapstudio user
RUN chmod 755 data logs backups exports uploads temp \
    && chown -R snapstudio:snapstudio /app

# Switch to non-root user
USER snapstudio

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5001/ || exit 1

# Default command
CMD ["python", "web_app.py"]
