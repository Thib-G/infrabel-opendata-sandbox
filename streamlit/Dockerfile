# app/Dockerfile

FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install -r requirements.txt

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "network.py", "--server.port=80", "--server.address=0.0.0.0"]
