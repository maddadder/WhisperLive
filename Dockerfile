FROM python:3.10-bookworm

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies for PyAudio and clean up
RUN apt update && \
    apt install -y portaudio19-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update pip to the latest version
RUN pip install --no-cache-dir -U "pip>=24"

# Create a working directory
WORKDIR /app

# Copy only the necessary files for the nvidia libraries; this can help with caching
COPY models/whisper-medium /app/models/whisper-medium

# Copy only the requirements file first, and install the dependencies
COPY requirements/server.txt /app/
RUN pip install --no-cache-dir -r server.txt && rm server.txt


# Set the environment variable for library paths (keeping it towards the end to avoid invalidating cache)
ENV LD_LIBRARY_PATH="/usr/local/lib/python3.10/site-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/site-packages/nvidia/cudnn/lib"

# Copy the application code last
COPY whisper_live /app/whisper_live
COPY run_server.py /app

# Define the command to run the server
CMD ["python", "run_server.py"]
