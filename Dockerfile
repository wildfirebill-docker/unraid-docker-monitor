FROM python:3.14-alpine

RUN echo 'https://dl-cdn.alpinelinux.org/alpine/edge/main' > /etc/apk/repositories && \
    echo 'https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories && \
    apk update && apk upgrade --no-cache -a && \
    pip install --no-cache-dir --break-system-packages docker flask

WORKDIR /app

COPY app.py .
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "app.py"]
