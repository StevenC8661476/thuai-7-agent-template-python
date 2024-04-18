# syntax=docker/dockerfile:1

FROM python:3.12.3-alpine3.19
WORKDIR /usr/local/src/app
COPY requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python", "main.py"]
