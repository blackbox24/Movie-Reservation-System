# Use a more specific, stable image tag
FROM python:3.12.3-slim AS builder

# Set the working directory
WORKDIR /usr/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for mysqlclient and other build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
       python3-dev \
    # Clean up APT cache to reduce image size
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY ./requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /usr/app/wheels -r requirements.txt

FROM python:3.12-slim


RUN groupadd --system myuser && useradd --system --gid myuser --shell /bin/false --no-create-home myuser

WORKDIR /usr/app

COPY --from=builder /usr/app/wheels /usr/app/wheels
COPY --from=builder /usr/app/requirements.txt /usr/app/


RUN pip install --no-cache-dir --no-index --find-links=/usr/app/wheels -r requirements.txt &&\
    rm -rf /usr/app/wheels

COPY . .

# Run your init script (if applicable)
RUN python manage.py collectstatic && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    chown -R myuser:myuser /usr/app

# Expose the Gunicorn port
USER myuser

EXPOSE 9000
