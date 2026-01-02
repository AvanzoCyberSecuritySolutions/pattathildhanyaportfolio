FROM python:3.11.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ✅ REQUIRED FOR mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

COPY . /app/

# 🔁 CHANGE "projectname" ONLY
CMD ["gunicorn", "pattathildhanya.wsgi:application", "--bind", "0.0.0.0:8000"]
