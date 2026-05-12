FROM python:3.11.9-slim

WORKDIR /app

ENV OLLAMA_HOST=http://host.docker.internal:11434

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY start.sh .
RUN sed -i 's/\r//' start.sh && chmod +x start.sh

RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8501
EXPOSE 8000

CMD ["./start.sh"]