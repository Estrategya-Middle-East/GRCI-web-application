# Setup server

# 1. Start Docker kernal + python
FROM python:3.11-slim-bullseye

# 2. ENV : show logs
ENV PYTHONUNBUFFERED=1

# 3. Update kernal + install dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libev-dev \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    && apt-get clean

# 4. Create project folder on kernal
WORKDIR /app

# 5. Copy the application files into the docker container
COPY . .

# 6. Install requirements
# Upgrade pip and install dependencies with higher timeout and retries
RUN pip install --no-cache-dir --upgrade pip setuptools wheel --timeout 300 --retries 5 -i https://pypi.org/simple
RUN pip install --no-cache-dir -r requirements.txt --timeout 300 --retries 5

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]