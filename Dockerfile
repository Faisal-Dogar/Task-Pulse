# 1. Lightweight Python base image
FROM python:3.11-slim

# 2. Environment variables taake Python buffer na kare aur bytecode na likhe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Container ke andar working directory set karein
WORKDIR /app

# 4. Dependencies install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application code copy karein
COPY . .

# 6. Port expose karein
EXPOSE 8000

# 7. FastAPI server run karein
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

