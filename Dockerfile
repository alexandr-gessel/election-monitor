# Python
FROM python:3.12-slim

# app folder
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy everything else
COPY . .

# environment
ENV PYTHONUNBUFFERED=1

# expose port
EXPOSE 8000

# run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
