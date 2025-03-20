FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

COPY . .
RUN pip install -r requirements.txt
RUN chmod +x run.sh

CMD ["sh","run.sh"]
