FROM apache/airflow:2.9.2
USER root
RUN  apt-get update \
&& apt-get install -y --no-install-recommends \
  wget \
  unzip \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver
RUN wget -N https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip -P /tmp && \
    unzip /tmp/chrome-linux64.zip && \
    mv /tmp/chrome-linux64/chromedriver /usr/local/bin && \
    rm /tmp/chrome-linux64.zip

COPY requirements.txt /

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

#RUN python3 -m venv /opt/venv

# Ensure the virtual environment is activated and install the requirements
#RUN /opt/venv/bin/pip install --no-cache-dir -r /requirements.txt

# Set the virtual environment as the default Python environment
#ENV PATH="/opt/venv/bin:$PATH"