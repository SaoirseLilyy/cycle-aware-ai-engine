FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY production/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --progress-bar off -r /app/requirements.txt

# Copy the production package as a package
COPY production /app/production

# Copy models
COPY models /app/models

# Expose API port
EXPOSE 8005

# IMPORTANT: run the correct module path
CMD ["uvicorn", "production.app:app", "--host", "0.0.0.0", "--port", "8005"]






