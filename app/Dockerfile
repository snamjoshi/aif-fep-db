FROM python:3.8

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

# RUN pip install numpy
# RUN pip install matplotlib

COPY aif-fep-db/app/ .
RUN python -m pip install -r requirements.txt

COPY aif-fep-db/src aif_fep_db/src

RUN chmod +x run.sh
CMD ["./run.sh"]