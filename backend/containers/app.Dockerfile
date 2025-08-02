FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
		build-essential \
		libpq-dev \
		&& rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["uvicorn", "src.app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
