FROM python:3.11-slim

# Security: avoid running as root
RUN useradd -m appuser

WORKDIR /app

# Install dependencies first (better caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/app.py .

# Switch to non-root user
USER appuser

EXPOSE 5000

# Gunicorn for production-style serving
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
