FROM python:3.9.7

WORKDIR /app
COPY app/ .

# COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY data/databases data/

RUN chmod +x run.sh
CMD ["./run.sh"]
