FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    python3-dev \
    libgl1 \
	libx11-6 \
	libxext-dev \
	libxrender-dev \
	libxinerama-dev \
	libxi-dev \
	libxrandr-dev \
	libxcursor-dev \
	libxtst-dev \
	tk-dev \
    libglib2.0-0 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=host.docker.internal:0.0

CMD ["python", "main.py"]
