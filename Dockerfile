FROM selenium/standalone-chromium:latest

USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    unzip

# Set the ChromeDriver version explicitly (match the Chrome version)
ARG CHROME_VERSION="126.0.6478.127"
ARG CHROMEDRIVER_VERSION="126.0.6478.126"

# Download and install ChromeDriver
RUN wget -N https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip -P /tmp && \
    unzip /tmp/chrome-linux64.zip -d /usr/local/bin && \
    rm /tmp/chrome-linux64.zip

COPY requirements.txt /

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv

# Ensure the virtual environment is activated and install the requirements
RUN /opt/venv/bin/pip install --no-cache-dir -r /requirements.txt

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

COPY dags/news_realtime.py /app/news_realtime.py

WORKDIR /app

CMD ["python3", "news_realtime.py"]