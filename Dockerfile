FROM python:3.11.5-slim-bullseye

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ✅ Required system packages (mysqlclient etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# ✅ REQUIRED for WhiteNoise (DO NOT SKIP)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start Django using Gunicorn
CMD ["gunicorn", "pattathildhanya.wsgi:application", "--bind", "0.0.0.0:8000"]