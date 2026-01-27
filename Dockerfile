# Base Image
FROM python:3.11-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Working Directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Application code ----------
COPY . .

# ---------- Vectorstore (baked into image) ----------
COPY data/vectorstore /app/vectorstore

# ---------- Expose port for Cloud Run ----------
EXPOSE 8080

# ---------- Run ----------
CMD ["python", "app.py"]