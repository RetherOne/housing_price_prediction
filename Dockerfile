FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi[standard]
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
