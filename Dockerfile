FROM python:3.11-alpine3.19

# curl required for entrypoint script
RUN apk add --no-cache curl

# python dependencies
COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /requirements.txt

# Copy app data
COPY . /app
WORKDIR /app

# Launch command
CMD ["sh", "/app/docker-entrypoint.sh"]

