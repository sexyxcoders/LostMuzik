FROM nikolaik/python-nodejs:python3.10-nodejs20-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    aria2 \
    libopus0 \
    libopus-dev \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip==24.0
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start"]