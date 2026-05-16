FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["uvicorn", "speech_coach.serving.api:app", "--host", "0.0.0.0", "--port", "8000"]
