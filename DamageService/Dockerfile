FROM python:3.11-slim

WORKDIR /app

# Kopiér requirements og installer dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér applikationsfiler
COPY . .

# Eksponér port
EXPOSE 5002

# Start med uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5002"]