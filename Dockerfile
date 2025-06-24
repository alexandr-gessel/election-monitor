# Python
FROM python:3.12-slim

# app folder
WORKDIR /app

# copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY alembic.ini .
COPY . .

# copy and start
COPY start.sh .
RUN chmod +x start.sh

# env
ENV PYTHONUNBUFFERED=1

# port
EXPOSE 8000

# run server
CMD ["./start.sh"]