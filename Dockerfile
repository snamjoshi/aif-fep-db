FROM python:3.8

WORKDIR /app

# RUN apt-get -y update && apt-get install -y \
#   python3-dev \
#   apt-utils \
#   python-dev \
#   build-essential \
# && rm -rf /var/lib/apt/lists/*

# RUN pip install numpy
# RUN pip install matplotlib

COPY app/ .
COPY src/ .
COPY requirements.txt .
# RUN python -m pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh
CMD ["./run.sh"]