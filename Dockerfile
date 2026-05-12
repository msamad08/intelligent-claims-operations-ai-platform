FROM python:3.11.9-slim

WORKDIR /app

ENV OLLAMA_HOST=http://host.docker.internal:11434

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8501
EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port 8000 & streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0"]