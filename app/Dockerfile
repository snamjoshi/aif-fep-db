FROM python:3.9.7

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
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# COPY src/ aif_fep_db/src/
COPY src/ src/
COPY data/databases data/

RUN chmod +x run.sh
CMD ["./run.sh"]
