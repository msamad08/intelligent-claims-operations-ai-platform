FROM python:3.11.9-slim

WORKDIR /app

ENV OLLAMA_HOST=http://host.docker.internal:11434

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8501
EXPOSE 8000

COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]

