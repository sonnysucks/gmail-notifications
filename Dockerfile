# SnapStudio Container for Cloudflare Deployment
# Professional Photography Business Management System

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/uploads /app/exports /app/backups

# Set environment variables
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:////app/data/web_app.db

# Create non-root user for security
RUN useradd -m -u 1000 snapstudio && \
    chown -R snapstudio:snapstudio /app
USER snapstudio

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start the application
CMD ["python", "web_app.py"]
