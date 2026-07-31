# [Docker Keyword] Pulls an official, security-patched, lean footprint Python runtime
FROM python:3.11-slim

# [Docker Keyword] Declares the primary directory container commands execute within
WORKDIR /app

ENV PYTHONPATH="/app:/app/src"

# [Docker Keyword] Standard Python optimization flags ensuring neat containers by halting file caching
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# [Docker Keyword] Installs system-level headers required to build the PostgreSQL database drivers from source
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# [Docker Keyword] Shifts the package requirements file first to take advantage of Docker cache layering
COPY requirements.txt .

# [Docker Keyword] Installs Python frameworks efficiently without dumping redundant data into the image
RUN pip install --no-cache-dir -r requirements.txt

# [Docker Keyword] Permanent step copying all remaining local application files into the image filesystem
COPY . .

# [Docker Keyword] Documents that the container application listens on port 8000
EXPOSE 8000

# [Docker Keyword] Runs the application natively without the performance penalty of the file-watching reload process
CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8000"]